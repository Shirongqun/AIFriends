<script setup>
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.js";
import Character from "@/components/character/Character.vue";
import {useRoute} from "vue-router";

const characters = ref([])
const isLoading = ref(false) // 防止同时发请求
const hasCharacters = ref(true) // 是否还有角色
const sentinelRef = useTemplateRef('sentinel-ref') // 哨兵的引用
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

// 循环加载
async function loadMore() {
  if (isLoading.value || !hasCharacters.value) return  // 正在加载或者没有更多角色
  isLoading.value = true

  let newCharacters = []  // 存储从云端加载的角色信息
  try {
    const res = await api.get('/api/homepage/index/', {
      params: {
        items_count: characters.value.length,
        search_query: route.query.q || '',
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newCharacters = data.characters  // 不是响应式变量，所以不用加 .value
    }
  } catch (err) {
  } finally {
    isLoading.value = false
    if (newCharacters.length === 0) {
      hasCharacters.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick()  // 等待元素渲染完成

      if (checkSentinelVisible()) {  // 确认哨兵是否能被看到
        await loadMore()
      }
    }
  }
}

let observer = null  // 定义监听器对象，监听什么时候哨兵出现
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            loadMore()
          }
        })
      },
      {root: null, rootMargin: '2px', threshold: 0}
  )

  observer.observe(sentinelRef.value)
})

function reset() {
  characters.value = []
  isLoading.value = false
  hasCharacters.value = true
  loadMore()
}

watch(() => route.query.q, newQ => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="flex flex-col items-center mb-12">
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
        v-for="character in characters"
        :key="character.id"
        :character="character"
      />
    </div>
    <!--  哨兵-->
    <div ref="sentinel-ref" class="h-2 mt-8"></div>
    <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
    <div v-if="!hasCharacters" class="text-gray-500">没有更多角色了</div>
  </div>
</template>

<style scoped>

</style>