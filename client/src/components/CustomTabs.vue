<template>
  <div class="flex flex-col md:flex-row gap-6">
    <div class="w-full md:w-64 flex-shrink-0">
      <ul class="flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-4 md:pb-0">
        <li v-for="(tab, i) in tabs" :key="i" class="shadow-md rounded-lg">
          <div
            @click="changeTab(i)"
            :class="[
              selectedTab === i
                ? 'bg-indigo-400 text-white shadow-md'
                : 'bg-white text-gray-600 hover:bg-gray-100',
              !isTabEnabled(i) ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
            ]"
            class="flex items-center justify-between py-3 px-4 rounded-lg font-medium transition-all"
          >
            <span>{{ tab.title }}</span>
            <span v-if="tab.done" class="text-xs">
              <CheckSvg fill="green" />
            </span>
          </div>
        </li>
      </ul>
    </div>

    <div class="p-6 rounded-lg flex-grow">
      <component
        :is="tabs[selectedTab]?.component"
        :category="tabs[selectedTab]?.category"
        @selection-made="markTabDone"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CheckSvg from './svg/CheckSvg.vue'

const props = defineProps<{ tabs: Record<string, unknown>[] }>()
const emit = defineEmits<{
  (e: 'stepDone'): void
  (e: 'tabChange', newTabIndex: number): void
}>()

const selectedTab = ref(0)

const isTabEnabled = (i: number) => i === 0 || props.tabs[i - 1]?.done
const changeTab = (i: number) => {
  if (isTabEnabled(i)) selectedTab.value = i
}

const markTabDone = () => {
  const tabsDone = props.tabs[selectedTab.value]

  if (tabsDone && !tabsDone.done) {
    tabsDone.done = true
  }

  if (selectedTab.value < props.tabs.length - 1) selectedTab.value++
  else {
    selectedTab.value = 0
    emit('stepDone')
  }
}
</script>
