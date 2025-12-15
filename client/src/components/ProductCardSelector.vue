<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div
      v-for="component in components"
      :key="component.id"
      @click="selectComponent(component)"
      :class="[
        isSelected(component.id) ? 'border-indigo-600 ring-2 ring-indigo-200' : 'border-gray-200',
      ]"
      class="relative bg-white border-2 rounded-xl p-4 cursor-pointer transition-all flex flex-col h-full shadow-md hover:border-indigo-400"
    >
      <div
        v-if="isSelected(component.id)"
        class="absolute -top-2 -right-2 bg-indigo-600 text-white rounded-full p-1 shadow-lg"
      >
        <CheckRoundedSvg />
      </div>

      <div class="flex-grow">
        <h4 class="font-bold text-gray-800">{{ component.name }}</h4>
        <p class="text-xs text-gray-500 uppercase tracking-tighter">{{ component.id }}</p>
      </div>

      <div class="mt-4 flex justify-between items-center border-t pt-3">
        <span class="text-sm font-semibold text-gray-700"
          >€ {{ getComponentPrice(component).toFixed(2) }}</span
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCatalogueStore } from '@/stores/catalogue'
import type { BikeComponent } from '@/types'
import CheckRoundedSvg from './svg/CheckRoundedSvg.vue'
import { storeToRefs } from 'pinia'

const props = defineProps<{ category: string }>()
const { selectedComponents } = storeToRefs(useCatalogueStore())
const { isComponentCompatible, setSelectedComponent, filteredCatalogue, getComponentPrice } =
  useCatalogueStore()
const emit = defineEmits(['selectionMade'])

const components = computed(() => filteredCatalogue(props.category) || [])

const isSelected = (id: string) => {
  return selectedComponents.value[props.category]?.id === id
}

const selectComponent = (comp: BikeComponent) => {
  if (isComponentCompatible(comp.id, props.category)) {
    setSelectedComponent(props.category, comp)
    emit('selectionMade')
  }
}
</script>
