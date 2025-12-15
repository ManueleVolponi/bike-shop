import apiAxios from '@/axios'

export async function check_price(payload: Record<string, unknown>) {
  const response = await apiAxios.post('/price/check', payload)

  return response.data
}
