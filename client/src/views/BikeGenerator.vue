<template>
  <div class="max-w-7xl mx-auto p-4">
    <div class="rounded-lg shadow-md mb-4 p-4">
      <!-- <div class="bg-gray-100 flex justify-center items-center min-h-[200px] w-full">
        Generator
      </div> -->

      <PriceComponent
        :current-base-price="currentBasePrice"
        :steps-length="steps.length"
        :current-step="currentStep"
      />

      <StepperComponent
        :steps="steps"
        :currentStep="currentStep"
        @step-change="currentStep = $event"
      />
    </div>
    <div class="bg-gray-50 rounded-xl p-6 min-h-[500px] shadow-md">
      <component
        :is="steps[currentStep]?.component"
        :stepTabs="allStepDefinitions[currentStep]"
        @step-done="stepsUpdate()"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onMounted, ref, reactive, shallowRef } from 'vue'
import StepperComponent from '@/components/StepperComponent.vue'
import SelectionComponent from '@/components/bikeGeneratorSteps/SelectionComponent.vue'
import ReviewConfirmationComponent from '@/components/bikeGeneratorSteps/ReviewConfirmationComponent.vue'
import { useCatalogueStore } from '@/stores/catalogue'
import PriceComponent from '@/components/PriceComponent.vue'
import ProductCardSelector from '@/components/ProductCardSelector.vue'

const { currentBasePrice } = storeToRefs(useCatalogueStore())
const { fetchConstraints, fetchCatalogue, fetchPricingRules } = useCatalogueStore()

onMounted(async () => {
  await fetchCatalogue()
  await fetchConstraints()
  await fetchPricingRules()
})

const steps = shallowRef([
  {
    title: 'Select Frame',
    component: SelectionComponent,
    categories: ['frame_type', 'frame_finish'],
    done: false,
  },
  {
    title: 'Choose Wheels',
    component: SelectionComponent,
    categories: ['wheels', 'rim_color'],
    done: false,
  },
  { title: 'Pick Accessories', component: SelectionComponent, categories: ['chain'], done: false },
  {
    title: 'Review & Confirm',
    component: ReviewConfirmationComponent,
    categories: [],
    done: false,
  },
])

const allStepDefinitions = reactive([
  [
    { title: 'Type', component: ProductCardSelector, category: 'frame_type', done: false },
    { title: 'Finish', component: ProductCardSelector, category: 'frame_finish', done: false },
  ],
  [
    { title: 'Wheels', component: ProductCardSelector, category: 'wheels', done: false },
    { title: 'Rim Color', component: ProductCardSelector, category: 'rim_color', done: false },
  ],
  [{ title: 'Chain', component: ProductCardSelector, category: 'chain', done: false }],
])

const currentStep = ref(0)

const stepsUpdate = () => {
  const currentStepObj = steps.value[currentStep.value]
  if (currentStepObj && !currentStepObj.done) {
    currentStepObj.done = true
  }
  currentStep.value++
}
</script>
