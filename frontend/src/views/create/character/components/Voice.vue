<script setup>
import {ref, watch} from "vue";

const props =defineProps(['voices', 'curVoiceId'])
const myVoice = ref(props.curVoiceId)

watch(() => props.curVoiceId, (newVal) => {
  myVoice.value = newVal
})

defineExpose({
  myVoice,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">音色</label>
<!--    下拉菜单-->
    <select v-model="myVoice" class="select">
      <option disabled selected>选择一个音色</option>
<!--      在html中使用无需加props，id、value传的没有问题-->
      <option
          v-for="voice in voices"
          :id="voice.id"
          :value="voice.id"
      >{{ voice.name }}</option>
    </select>
  </fieldset>
</template>

<style scoped>

</style>