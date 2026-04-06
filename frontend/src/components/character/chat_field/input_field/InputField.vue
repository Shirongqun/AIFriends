<script setup>

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {onUnmounted, ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
let processId = 0  // 全局变量，可用于标识当前聊天窗口中新加入对话的版本号
const showMic = ref(false) // 是否显示语音输入模块

let mediaSource = null;
let sourceBuffer = null;
let audioPlayer = new Audio(); // 全局播放器实例
let audioQueue = [];           // 待写入 Buffer 的二进制队列
let isUpdating = false;        // Buffer 是否正在写入

const initAudioStream = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    mediaSource = new MediaSource();
    audioPlayer.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
        try {
            sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
            sourceBuffer.addEventListener('updateend', () => {
                isUpdating = false;
                processQueue();
            });
        } catch (e) {
            console.error("MSE AddSourceBuffer Error:", e);
        }
    });

    audioPlayer.play().catch(e => console.error("等待用户交互以播放音频"));
};

const processQueue = () => {
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
        return;
    }

    isUpdating = true;
    const chunk = audioQueue.shift();
    try {
        sourceBuffer.appendBuffer(chunk);
    } catch (e) {
        console.error("SourceBuffer Append Error:", e);
        isUpdating = false;
    }
};

const stopAudio = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                mediaSource.endOfStream();
            } catch (e) {
            }
        }
        mediaSource = null;
    }

    if (audioPlayer.src) {
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

const handleAudioChunk = (base64Data) => {  // 将语音片段添加到播放器队列中
    try {
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        audioQueue.push(bytes);
        processQueue();
    } catch (e) {
        console.error("Base64 Decode Error:", e);
    }
};

onUnmounted(() => {
    audioPlayer.pause();
    audioPlayer.src = '';
});

function focus() {
  inputRef.value.focus()
}

// 1、绑定到表单、发送按钮，提交表单或者点击发送按钮后被调用
// 2、绑定到了Microphone.vue，子组件里成功调用后端语音识别得到文本后也会调用该函数
// 3、event是默认传入的参数，不能省略
async function handleSend(event, audio_msg) {
  // 取出内容
  let content
  if (audio_msg) { // 语音识别后的文字
    content = audio_msg.trim()
  } else {
    content = message.value.trim()
  }
  if (!content) return

  // 初始化音频播放器
  initAudioStream()

  const curId = ++ processId // 先+1，再赋值给curId
  message.value = ''

  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})

  try {
    await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content
      },
      // isDone: 自定义的标识数据是否已经发送结束
      onmessage(data, isDone) {
        if (curId !== processId) return

        if (data.content) {
          emit('addToLastMessage', data.content)
        }
        // 处理音频
        if (data.audio) {
          handleAudioChunk(data.audio)
        }
      },
      onerror(err) {
      },
    })
  } catch (err) {
  }
}

// 关闭输入模块组件
function close() {
  ++ processId  // 所有旧的对话都不再接受消息了
  showMic.value = false
  stopAudio()
}

// 打断虚拟角色说话
function handleStop() {
  ++ processId
  stopAudio()
}

// 将接口暴漏给父组件
defineExpose({
  focus,
  close,
})
</script>

<template>
<!--  文本输入模块-->
  <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
<!--    文本输入框-->
    <input
      ref="input-ref"
      v-model="message"
      class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
      type="text"
      placeholder="文本输入..."
    >
<!--    小麦克风-->
    <div @click="showMic = true" class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
<!--    发送-->
    <div @click="handleSend" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon />
    </div>
  </form>
<!--  语音输入模块-->
  <Microphone
      v-else
      @close="showMic = false"
      @send="handleSend"
      @stop="handleStop"
  />
</template>

<style scoped>

</style>