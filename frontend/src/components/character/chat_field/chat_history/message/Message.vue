<script setup>
import {useUserStore} from "@/stores/user.js";

defineProps(['message', 'character'])

const user = useUserStore()
</script>

<template>
  <div v-if="message.content">
<!--    ai发言-->
    <div v-if="message.role === 'ai'" class="chat chat-start">
      <div class="chat-image avatar">
        <div class="w-10 rounded-full">
          <img :src="character.photo" alt="">
        </div>
      </div>
<!--      聊天泡泡-->
      <div class="chat-bubble whitespace-pre-wrap break-all">{{ message.content }}</div>
    </div>
<!--    用户发言-->
    <div v-else class="chat chat-end">
      <div class="chat-image avatar">
        <div class="w-10 rounded-full">
          <img :src="user.photo" alt="">
        </div>
      </div>
<!--      聊天泡泡-->
      <div class="chat-bubble chat-bubble-success whitespace-pre-wrap">{{ message.content }}</div>
    </div>
  </div>
</template>

<style scoped>

</style>