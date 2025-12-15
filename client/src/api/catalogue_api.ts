import apiAxios from '@/axios'

export async function get_full_catalogue() {
  const response = await apiAxios.get('/catalogue/full')

  return response.data || []
}

export async function get_constraints() {
  const response = await apiAxios.get('/catalogue/constraints')

  return response.data || {}
}

export async function get_pricing_rules() {
  const response = await apiAxios.get('/catalogue/pricing_rules')

  return response.data || {}
}
