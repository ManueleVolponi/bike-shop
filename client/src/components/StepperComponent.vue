<template>
  <div class="w-full">
    <ol
      class="lg:flex items-center w-full space-y-4 lg:space-x-8 lg:space-y-0"
      :class="mainClasses"
    >
      <li
        class="flex-1 px-2 cursor-pointer"
        v-for="(step, i) in steps"
        :key="i"
        @click="changeStep(i)"
      >
        <div
          class="border-l-2 flex flex-col border-t-0 pl-4 pt-0 border-solid font-medium lg:pt-4 lg:border-t-2 lg:border-l-0 lg:pl-0"
          :class="{
            'border-indigo-600': i === currentStep, // Active
            'border-green-600': i < currentStep, // Done
            'border-gray-300': i > currentStep, // Pending
            [itemClasses]: true,
          }"
        >
          <span
            class="text-sm lg:text-base"
            :class="i <= currentStep ? 'text-indigo-600' : 'text-gray-400'"
            >Step {{ i + 1 }}</span
          >
          <h4 class="text-base lg:text-lg text-gray-900">{{ step.title }}</h4>
        </div>
      </li>
    </ol>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'stepChange', stepIndex: number): void
}>()

const props = withDefaults(
  defineProps<{
    steps: { title: string; component: unknown; categories: string[]; done: boolean }[]
    currentStep: number
    mainClasses?: string
    itemClasses?: string
  }>(),
  {
    mainClasses: '',
    itemClasses: '',
  },
)

function changeStep(i: number) {
  if (props.steps[i]?.done || props.steps[i - 1]?.done) {
    emit('stepChange', i)
  }
}
</script>
