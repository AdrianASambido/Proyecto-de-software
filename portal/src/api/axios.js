import axios from 'axios'

const BASE_URL = import.meta.env.VITE_BASE_URL || "https://admin-grupo01.proyecto2025.linti.unlp.edu.ar/api"

const api=axios.create({
  baseURL: BASE_URL
})

// Interceptor para agregar token si existe
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')

      setTimeout(() => {
        window.location.href = '/login'
      }, 1500)
    } else if (error.response?.status === 403) {
      toast.error('No tienes permisos para realizar esta acción')
    }

    return Promise.reject(error)
  }
)

export default api