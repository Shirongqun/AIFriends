import asyncio
import base64
import json
import os
import threading
import uuid
from queue import Queue

import websockets
from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk, SystemMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import ChatGraph
from web.views.friend.message.memory.update import update_memory


class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

# 添加系统提示词
def add_system_prompt(state, friend):
    msgs = state['messages'] # 用户的最新消息
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    prompt += f'\n【角色性格】\n{friend.character.profile}\n'
    prompt += f'【长期记忆】\n{friend.memory}\n'
    return {'messages': [SystemMessage(prompt)] + msgs}

# 添加最近的十轮对话
def add_recent_messages(state, friend):
    msgs = state['messages']
    # 读取最近的十轮对话
    message_raw = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()
    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    return {'messages': msgs[:1] + messages + msgs[-1:]}

class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]  # 引入渲染器
    def post(self, request):
        """处理前端传入"""
        friend_id = request.data['friend_id']     # 数据库自带的id，可唯一确定与虚拟角色的好友关系
        message = request.data['message'].strip() # 用户发送的消息
        if not message:
            return Response({
                'result': '消息不能为空',
            })
        friends = Friend.objects.filter(id=friend_id, me__user=request.user) # pk 跟 id 一样
        if not friends.exists():
            return Response({
                'result': '好友不存在',
            })
        friend = friends.first()
        app = ChatGraph.create_app()

        inputs = {
            'messages': [HumanMessage(message)],
        }
        inputs = add_system_prompt(inputs, friend)
        inputs = add_recent_messages(inputs, friend)

        response = StreamingHttpResponse(
            self.event_stream(app, inputs, friend, message),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no' # 不让Nginx缓存流式信息
        return response

    # app: 文本生成的Graph
    # inputs: 要发给文本大模型的输入
    # mq: 存放语音合成结果
    # ws: 建立与阿里云 DashScope 的实时推理接口
    # task_id:
    async def tts_sender(self, app, inputs, mq, ws, task_id):
        """利用文本大模型生成要回复的文字，并将其传给语音大模型"""
        async for msg, metadata in app.astream(inputs, stream_mode="messages"):
            if isinstance(msg, BaseMessageChunk):
                if msg.content:
                    # 发给语音合成大模型
                    await ws.send(json.dumps({
                        "header": {
                                      "action": "continue-task",
                                      "task_id": task_id, # 随机uuid
                        "streaming": "duplex"
                    },
                        "payload": {
                        "input": {
                            "text": msg.content,
                        }
                    }
                    }))
                    # 放到消息队列中
                    mq.put_nowait({'content': msg.content})
                if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                    mq.put_nowait({'usage': msg.usage_metadata})
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {} # input不能省去，否则会报错
        }
        }))

    async def tts_receiver(self, mq, ws):
        # 每次迭代都 await 下一条消息
        async for msg in ws:
            # 如果返回的是字节数据
            if isinstance(msg, bytes):
                # 将音频使用base64编码成文本
                audio = base64.b64encode(msg).decode('utf-8')
                mq.put_nowait({'audio': audio})
            else:
                data = json.loads(msg)
                event = data['header']['event']
                if event in ['task-finished', 'task-failed']:
                    break

    # 副线程需要定义一些协程
    async def run_tts_tasks(self, app, inputs, mq, voice_id):
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "action": "run-task",
                    "task_id": task_id,  # 随机uuid
                    "streaming": "duplex"
                },
                "payload": {
                    "task_group": "audio",
                    "task": "tts", # 语音合成
                    "function": "SpeechSynthesizer",
                    "model": "cosyvoice-v3-flash",
                    "parameters": {
                        "text_type": "PlainText",
                        "voice": voice_id,  # 音色
                        "format": "mp3",  # 音频格式
                        "sample_rate": 22050,  # 采样率
                        "volume": 50,  # 音量
                        "rate": 1.25,  # 语速
                        "pitch": 1  # 音调
                    },
                    "input": {  # input不能省去，不然会报错
                    }
                }
            }))
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break
            await asyncio.gather(
                self.tts_sender(app, inputs, mq, ws, task_id),
                self.tts_receiver(mq, ws),
            )

    def work(self, app, inputs, mq, voice_id):
        try:
            asyncio.run(self.run_tts_tasks(app, inputs, mq, voice_id))
        finally:
            mq.put_nowait(None)

    def event_stream(self, app, inputs, friend, message):
        mq = Queue()
        # 创建副线程
        thread = threading.Thread(target=self.work, args=(app, inputs, mq, friend.character.voice.voice_id))
        thread.start()

        full_output = '' # 大模型的回复
        full_usage = {}  # 消耗量
        while True:
            msg = mq.get()
            if not msg:
                break
            if msg.get('content', None):
                full_output += msg['content']
                yield f'data: {json.dumps({'content': msg['content']}, ensure_ascii=False)}\n\n'
            if msg.get('audio', None):
                yield f'data: {json.dumps({'audio': msg['audio']}, ensure_ascii=False)}\n\n'
            # token的消耗量
            if msg.get('usage', None):
                full_usage = msg['usage']

        yield f'data: [DONE]\n\n'
        input_tokens = full_usage.get('input_tokens', 0)
        output_tokens = full_usage.get('output_tokens', 0)
        total_tokens = full_usage.get('total_tokens', 0)
        Message.objects.create(
            friend=friend,
            user_message=message[:500],
            input=json.dumps(
                [m.model_dump() for m in inputs['messages']],
                ensure_ascii=False,
            )[:10000],
            output=full_output[:500],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )
        # 每间隔10条对话就保存一次记忆
        if Message.objects.filter(friend=friend).count() % 1 == 0:
            update_memory(friend)