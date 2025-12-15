export interface Bike {
  frameType: BikeComponent
  frameFinish: BikeComponent
  wheels: BikeComponent
  rimColor: BikeComponent
  chain: BikeComponent
  price: number
}

export interface BikeComponent {
  id: string
  name: string
  category: string
  price: number
}

export interface Selector {
  category: string
  id: string
}

export interface Effect {
  type: 'FIXED_PRICE' | 'PERCENTAGE_DISCOUNT'
  target_category: string
  target_id: string
  value: number
}

export interface PricingRule {
  selectors: Selector[]
  effect: Effect
}
