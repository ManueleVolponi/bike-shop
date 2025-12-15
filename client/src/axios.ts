import axios from 'axios'

const apiAxios = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  withCredentials: true,
})

export default apiAxios
