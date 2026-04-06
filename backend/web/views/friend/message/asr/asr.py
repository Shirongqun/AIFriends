import asyncio
import json
import os
import uuid

import websockets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ASRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 从前段接收数据
        audio = request.FILES.get('audio')
        if not audio:
            return Response({
                'result': '音频不存在',
            })
        pcm_data = audio.read()
        # 调用协程，即打开一个事件循环，这里是同步等待
        # asyncio.run() 是连接同步和异步世界的桥梁
        # asyncio.run() 方式：事件循环驱动
        text = asyncio.run(self.run_asr_tasks(pcm_data)) # 返回文本
        return Response({
            'result': 'success',
            'text': text,
        })
    # 语音识别发送数据
    async def asr_send(self, pcm_data, ws, task_id):
        chunk = 3200
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i + chunk])
            await asyncio.sleep(0.01) # 等待10ms，不是100ms，更快
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }))
    # 语音识别接受数据
    async def asr_receiver(self, ws):
        text = ''
        async for msg in ws:
            data = json.loads(msg)
            event = data['header']['event']
            if event == 'result-generated':
                output = data['payload']['output']
                if output.get('transcription', None) and output['transcription']['sentence_end']:
                    text += output['transcription']['text']
            elif event in ['task-finished', 'task-failed']:
                break
        return text

    # 异步函数
    async def run_asr_tasks(self, pcm_data):
        # 创建task_id
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        # 定义鉴权头
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        # 创建一个异步websocket
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",
                    "task_id": task_id,
                    "action": "run-task"
                },
                "payload": {
                    "model": "gummy-realtime-v1",
                    "parameters": {
                        "sample_rate": 16000,
                        "format": "pcm",
                        "transcription_enabled": True, # 识别
                    },
                    "input": {},
                    "task": "asr",
                    "task_group": "audio",
                    "function": "recognition"
                }
            }))
            # 异步请求要用异步循环，把ws挂起，直到收到结果后继续执行
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break
            # 2个协程同时执行
            _, text = await asyncio.gather(
                self.asr_send(pcm_data, ws, task_id),
                self.asr_receiver(ws)
            )
            # 等待以上协程全部执行完毕，再返回文本
            return text