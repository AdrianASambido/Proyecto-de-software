import { ref } from 'vue'
import api from '@/api/axios'
import { toast } from 'vue-sonner'

export function useReviews() {
  const loading = ref(false)

  const createReview = async (siteId, data) => {
    loading.value = true
    try {
      const response = await api.post(`/sites/${siteId}/reviews`, data)
      toast.success('Reseña enviada. Será revisada antes de publicarse.')
      return response.data
    } catch (error) {
      if (error.response?.status === 400) {
        toast.error(error.response.data.error || 'Datos inválidos')
      } else if (error.response?.status === 401) {
        toast.error('Debes iniciar sesión para crear una reseña')
      } else {
        toast.error('Error al crear la reseña. Intenta nuevamente.')
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  const deleteReview = async (siteId, reviewId) => {
    loading.value = true
    try {
      await api.delete(`/sites/${siteId}/reviews/${reviewId}`)
      toast.success('Reseña eliminada exitosamente')
      return true
    } catch (error) {
      if (error.response?.status === 403) {
        toast.error('No tienes permisos para eliminar esta reseña')
      } else if (error.response?.status === 404) {
        toast.error('Reseña no encontrada')
      } else if (error.response?.status === 401) {
        toast.error('Debes iniciar sesión')
      } else {
        toast.error('Error al eliminar la reseña')
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  const updateReview = async (siteId, reviewId, data) => {
    loading.value = true
    try {
      const response = await api.put(`/sites/${siteId}/reviews/${reviewId}`, data)
      toast.success('Reseña actualizada exitosamente')
      return response.data
    } catch (error) {
      if (error.response?.status === 400) {
        toast.error(error.response.data.error || 'Datos inválidos')
      } else if (error.response?.status === 403) {
        toast.error('No puedes editar esta reseña')
      } else if (error.response?.status === 404) {
        toast.error('Reseña no encontrada')
      } else if (error.response?.status === 401) {
        toast.error('Debes iniciar sesión')
      } else {
        toast.error('Error al actualizar la reseña')
      }
      throw error
    } finally {
      loading.value = false
    }
  }

  const checkUserHasReview = async (siteId) => {
    try {
      const response = await api.get('/me/reviews')

      if (!response.data.data) return null

      const userReview = response.data.data.find(
        review => review.site_id === siteId
      )
      return userReview || null
    } catch (error) {
      console.error('Error checking user review:', error)
      return null
    }
  }

  return {
    loading,
    createReview,
    deleteReview,
    updateReview,
    checkUserHasReview
  }
}
