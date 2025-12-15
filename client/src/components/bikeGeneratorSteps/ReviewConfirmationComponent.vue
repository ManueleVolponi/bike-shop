<template>
  <div class="max-w-2xl mx-auto">
    <h2 class="text-3xl font-black text-gray-800 mb-6 text-center">Configuration Review</h2>

    <div class="bg-white border rounded-2xl overflow-hidden shadow-sm mb-8">
      <div
        v-for="(comp, category) in selectedComponents"
        :key="category"
        class="flex items-center justify-between p-4 border-b last:border-b-0"
      >
        <div class="flex items-center gap-4">
          <div>
            <p class="text-[10px] uppercase font-bold text-indigo-500 tracking-wider">
              {{ category.replace('_', ' ') }}
            </p>
            <h4 class="font-bold text-gray-800">{{ comp?.name || 'Not selected' }}</h4>
          </div>
        </div>

        <div class="text-right">
          <p class="font-mono font-bold text-gray-700">
            € {{ comp ? getComponentPrice(comp).toFixed(2) : '0.00' }}
          </p>
          <span
            v-if="comp && getComponentPrice(comp) !== comp.price"
            class="text-[9px] bg-green-100 text-green-700 p-1 rounded font-bold uppercase"
          >
            Rule Applied Price
          </span>
        </div>
      </div>

      <div class="bg-gray-50 p-6 flex justify-between items-center">
        <span class="text-lg font-bold text-gray-600">Final Price</span>
        <span class="text-4xl font-black text-indigo-700 tracking-tight">
          € {{ currentBasePrice.toFixed(2) }}
        </span>
      </div>
    </div>

    <div class="space-y-4">
      <button
        @click="confirmOrder"
        :disabled="isSubmitting"
        class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white rounded-xl font-bold text-lg shadow-lg transition-all flex justify-center items-center gap-3"
      >
        <span v-if="isSubmitting" class="text-2xl">⏳</span>
        {{ isSubmitting ? 'Checking...' : 'Confirm and Send' }}
      </button>

      <div
        v-if="serverMessage"
        :class="
          serverMessage.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        "
        class="p-4 rounded-xl border text-center font-medium"
      >
        {{ serverMessage.text }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCatalogueStore } from '@/stores/catalogue'
import { check_price } from '@/api/orders_api'
import { storeToRefs } from 'pinia'

const { selectedComponents, currentBasePrice } = storeToRefs(useCatalogueStore())
const { getComponentPrice } = useCatalogueStore()
const isSubmitting = ref(false)
const serverMessage = ref<{ type: 'success' | 'error'; text: string } | null>(null)

const confirmOrder = async () => {
  isSubmitting.value = true
  serverMessage.value = null

  try {
    const payload = {
      component_ids: Object.values(selectedComponents.value).map((c) => c?.id),
      client_total: currentBasePrice.value,
    }

    const response = await check_price(payload)

    if (response.valid) {
      serverMessage.value = {
        type: 'success',
        text: `Order confirmed!: € ${response.final_price}`,
      }
    } else {
      serverMessage.value = {
        type: 'error',
        text: 'Error: Something went wrong.',
      }
    }
  } catch (error) {
    serverMessage.value = { type: 'error', text: `${error}` }
  } finally {
    isSubmitting.value = false
  }
}
</script>
