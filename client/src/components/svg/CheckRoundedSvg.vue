<template>
  <div>
    <svg :class="classes" :fill="fill" :stroke="stroke" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="3"
        d="M5 13l4 4L19 7"
      ></path>
    </svg>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    classes?: string
    fill?: string
    stroke?: string
  }>(),
  {
    classes: 'w-5 h-5',
    fill: 'none',
    stroke: 'currentColor',
  },
)
</script>
