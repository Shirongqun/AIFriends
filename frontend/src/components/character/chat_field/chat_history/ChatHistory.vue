<script setup>
import Message from "@/components/character/chat_field/chat_history/message/Message.vue";
import {nextTick, onBeforeUnmount, onMounted, useTemplateRef} from "vue";
import api from "@/js/http/api.js";

const props = defineProps(['history', 'friendId', 'character'])
const emit = defineEmits(['pushFrontMessage'])
const scrollRef = useTemplateRef('scroll-ref')
const sentinelRef = useTemplateRef('sentinel-ref')
let isLoading = false  // 没有用在页面布局，所以不采用响应式变量
let hasMessages = true
let lastMessageId = 0

// 判断哨兵是否能被看到：判断哨兵是否跟scrollRef标签有交集
function checkSentinelVisible() {
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}

async function loadMore() {
  if (isLoading || !hasMessages) return
  isLoading = true

  let newMessages = []
  try {
    const res = await api.get('/api/friend/message/get_history/', {
      params: {
        last_message_id: lastMessageId,
        friend_id: props.friendId,
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newMessages = data.messages
    }
  } catch (err) {
  } finally {
    isLoading = false

    if (newMessages.length === 0) {
      hasMessages = false
    } else {
      const oldHeight = scrollRef.value.scrollHeight  // 加载前的scroll高度
      const oldTop = scrollRef.value.scrollTop
      for (const m of newMessages) {
        emit('pushFrontMessage', {
          role: 'ai',
          content: m.output,
          id: crypto.randomUUID(),
        })
        emit('pushFrontMessage', {
          role: 'user',
          content: m.user_message,
          id: crypto.randomUUID(),
        })
        lastMessageId = m.id
      }

      await nextTick()

      const newHeight = scrollRef.value.scrollHeight  // 加载后的scroll高度
      scrollRef.value.scrollTop = oldTop + (newHeight - oldHeight)

      // 加完后再判断哨兵是否被看到
      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(
      entries => {  // 可见性发生变化时才会回调
        entries.forEach(entry => {
          if (entry.isIntersecting) {  // 被监听元素可见
            loadMore()
          }
        })
      },
      {root: null, rootMargin: '2px', threshold: 0}
  )

  // 创建监听器监听哨兵，仅当其可见性发生变化时调用监听器的回调函数
  observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
})

// 聊天记录自动滚动到底部，每次添加完消息后触发
async function scrollToBottom() {
  await nextTick()

  scrollRef.value.scrollTop = scrollRef.value.scrollHeight
}

// 把scrollToBottom暴露给父组件ChatField.vue
defineExpose({
  scrollToBottom,
})
</script>

<template>
  <div ref="scroll-ref" class="absolute top-18 left-0 w-90 h-112 overflow-y-scroll no-scrollbar">
    <div ref="sentinel-ref" class="h-2"></div>
    <Message
        v-for="message in history"
        :key="message.id"
        :message="message"
        :character="character"
    />
  </div>
</template>

<style scoped>
/* 隐藏 Chrome, Safari 和 Opera 的滚动条 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 隐藏 IE, Edge 和 Firefox 的滚动条 */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>