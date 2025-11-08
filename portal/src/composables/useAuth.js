import { ref, computed } from 'vue'

// Estado global de autenticación (simplificado)
const isAuthenticated = ref(false)
const currentUser = ref(null)

export function useAuth() {
  // Verificar si hay sesión (simplificado - en producción debería verificar con el backend)
  const checkAuth = async () => {
    try {
      // Aquí podrías hacer una petición al backend para verificar la sesión
      // Por ahora, simplemente verificamos si hay un token en localStorage
      const token = localStorage.getItem('auth_token')
      isAuthenticated.value = !!token
      
      // Si hay token, intentar obtener información del usuario
      if (token) {
        // Aquí podrías hacer una petición para obtener el usuario actual
        // Por ahora, solo marcamos como autenticado
      }
    } catch (error) {
      console.error('Error verificando autenticación:', error)
      isAuthenticated.value = false
    }
  }

  // Inicializar al cargar
  checkAuth()

  return {
    isAuthenticated: computed(() => isAuthenticated.value),
    currentUser: computed(() => currentUser.value),
    checkAuth,
    setAuth: (authenticated, user = null) => {
      isAuthenticated.value = authenticated
      currentUser.value = user
    }
  }
}

