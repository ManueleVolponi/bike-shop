<template>
  <div>
    <CustomTabs :tabs="stepTabs" @step-done="emit('stepDone')" />
  </div>
</template>

<script setup lang="ts">
import CustomTabs from '../CustomTabs.vue'

defineProps<{
  stepTabs: Record<string, string>[]
}>()

const emit = defineEmits<{
  (e: 'stepDone'): void
}>()
</script>
