import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import type { BikeComponent, PricingRule, Selector } from '@/types'
import { get_full_catalogue, get_constraints, get_pricing_rules } from '@/api/catalogue_api'

type SelectionMap = Record<string, BikeComponent | undefined>

export const useCatalogueStore = defineStore('catalogue', () => {
  const catalogue = ref<Record<string, BikeComponent[]>>({})
  const constraints = ref<Record<string, Record<string, string[]>>>({})
  const pricingRules = ref<PricingRule[]>([])

  const selectedComponents = ref<SelectionMap>({
    frame_type: undefined,
    frame_finish: undefined,
    wheels: undefined,
    rim_color: undefined,
    chain: undefined,
  })

  async function fetchCatalogue() {
    try {
      const data = await get_full_catalogue()
      catalogue.value = data
    } catch (error) {
      console.error(error)
    }
  }

  async function fetchConstraints() {
    const response = await get_constraints()
    constraints.value = response
  }

  function setSelectedComponent(category: keyof SelectionMap, component: BikeComponent) {
    selectedComponents.value[category] = component
  }

  const isComponentCompatible = computed(() => (currentId: string, currentCategory: string) => {
    const selection = selectedComponents.value
    const constraintsMap = constraints.value

    for (const [selCategory, selComponent] of Object.entries(selection)) {
      if (selComponent && selCategory !== currentCategory) {
        const triggerId = selComponent.id
        const exclusionsFromSelection = constraintsMap[triggerId]

        if (exclusionsFromSelection && exclusionsFromSelection[currentCategory]) {
          if (exclusionsFromSelection[currentCategory].includes(currentId)) {
            return false
          }
        }
      }
    }

    const exclusionsFromCurrent = constraintsMap[currentId]
    if (exclusionsFromCurrent) {
      for (const [affectedCategory, excludedIds] of Object.entries(exclusionsFromCurrent)) {
        const alreadySelected = selection[affectedCategory as keyof SelectionMap]

        if (alreadySelected && excludedIds.includes(alreadySelected.id)) {
          return false
        }
      }
    }

    return true
  })

  const filteredCatalogue = computed(() => (category: string) => {
    const fullList = catalogue.value[category] || []

    return fullList.filter((component) => {
      return isComponentCompatible.value(component.id, category)
    })
  })

  async function fetchPricingRules() {
    const response = await get_pricing_rules()
    pricingRules.value = response
  }

  const getComponentPrice = computed(() => (component: BikeComponent) => {
    const activeRule = pricingRules.value.find((rule) => {
      const effect = rule.effect

      if (effect.target_category === component.category && effect.target_id === component.id) {
        return rule.selectors.every((selector: Selector) => {
          return selectedComponents.value[selector.category]?.id === selector.id
        })
      }
      return false
    })

    if (activeRule) {
      if (activeRule.effect.type === 'FIXED_PRICE') {
        return activeRule.effect.value
      }
      if (activeRule.effect.type === 'PERCENTAGE_DISCOUNT') {
        return component.price * (1 - activeRule.effect.value / 100)
      }
    }

    return component.price
  })

  const currentBasePrice = computed(() => {
    return Object.values(selectedComponents.value).reduce((total, comp) => {
      if (!comp) return total
      return total + getComponentPrice.value(comp)
    }, 0)
  })

  watch(
    selectedComponents,
    (newSelection) => {
      for (const [category, component] of Object.entries(newSelection)) {
        if (component && !isComponentCompatible.value(component.id, category)) {
          selectedComponents.value[category as keyof SelectionMap] = undefined
        }
      }
    },
    { deep: true },
  )

  return {
    catalogue,
    constraints,
    selectedComponents,
    currentBasePrice,
    isComponentCompatible,
    getComponentPrice,
    pricingRules,
    filteredCatalogue,

    fetchCatalogue,
    fetchConstraints,
    setSelectedComponent,
    fetchPricingRules,
  }
})
