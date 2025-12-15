<template>
  <div class="sticky top-0 z-50 bg-white p-4 mb-4 flex justify-between items-center">
    <div>
      <h2 class="text-xl font-bold">Bike Configurator</h2>
      <p class="text-sm text-gray-500">Step {{ currentStep + 1 }} of {{ stepsLength }}</p>
    </div>
    <div class="text-right">
      <span class="text-gray-600 mr-2 uppercase text-xs font-bold tracking-widest"
        >Current Price:</span
      >
      <span class="text-3xl font-black text-indigo-600">€ {{ currentBasePrice.toFixed(2) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  currentStep: number
  stepsLength: number
  currentBasePrice: number
}>()
</script>
