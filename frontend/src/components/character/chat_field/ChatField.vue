<script setup>
// 从父组件传过来的信息
import {computed, nextTick, ref, useTemplateRef} from "vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

const props = defineProps(['friend'])
// 定义模态框引用
const modalRef = useTemplateRef('modal-ref')
// 输入框引用
const inputRef = useTemplateRef('input-ref')
// 聊天框引用
const chatHistoryRef = useTemplateRef('chat-history-ref')
// 历史消息
const history = ref([])

// 异步函数
async function showModal() {
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

// 在最后添加一条消息
function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

// 在最后一条消息上添加内容，AI的流式回复
function handleAddToLastMessage(delta) {
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

// 往上加消息
function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

function handleClose() {
  inputRef.value.close()
}

defineExpose({
  showModal,
})
</script>

<!--聊天模态框-->
<template>
  <dialog ref="modal-ref" class="modal" @close="handleClose">
    <div class="modal-box w-90 h-150" :style="modalStyle">
<!--      关闭按钮-->
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">✕</button>
<!--      角色头像-->
      <CharacterPhotoField v-if="friend" :character="friend.character"/>
<!--      历史聊天窗口-->
      <ChatHistory
          ref="chat-history-ref"
          v-if="friend"
          :history="history"
          :friendId="friend.id"
          :character="friend.character"
          @pushFrontMessage="handlePushFrontMessage"
      />
      <InputField
          v-if="friend"
          ref="input-ref"
          :friendId="friend.id"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
      />
    </div>
  </dialog>
</template>

<style scoped>

</style>