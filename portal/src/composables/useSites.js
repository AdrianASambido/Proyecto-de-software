import { ref } from 'vue'
import api from '@/api/axios'

export function useSites() {
  const loading = ref(false)
  const error = ref(null)

  const fetchSites = async (params = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const defaultParams = {
        page: 1,
        per_page: 8, // Limitar a 8 para las secciones del home
        include_cover: 'true' // Debe ser string 'true' según el backend
      }
      
      // Merge de params, pero asegurarse de que include_cover sea string si se especifica
      const finalParams = { ...defaultParams, ...params }
      // Siempre asegurar que include_cover sea 'true' como string
      if (finalParams.include_cover === undefined || finalParams.include_cover === null) {
        finalParams.include_cover = 'true'
      } else {
        finalParams.include_cover = String(finalParams.include_cover)
      }
      
      console.log('Fetching sites with params:', finalParams)
      const { data } = await api.get('/sites', { params: finalParams })
      console.log('Sites fetched:', data.data?.length || 0, 'sites')
      if (data.data && data.data.length > 0) {
        console.log('First site cover_url:', data.data[0].cover_url)
      }
      return data.data || []
    } catch (err) {
      console.error('Error fetching sites:', err)
      console.error('Error response:', err.response?.data)
      error.value = err.response?.data?.error || 'Error al cargar los sitios'
      return []
    } finally {
      loading.value = false
    }
  }

  const fetchMejorPuntuados = async () => {
    return await fetchSites({ order: 'mejor_puntuado' })
  }

  const fetchRecientementeAgregados = async () => {
    return await fetchSites({ order: 'fecha_desc' })
  }

  const fetchFavoritos = async (userId = null) => {
    // Nota: El backend puede requerir user_id en los filtros para favoritos
    // Si el backend usa JWT/sesión, puede obtener el user_id del token/sesión automáticamente
    // Intentamos cargar con favoritos=true y, si hay userId, lo incluimos
    const params = { favoritos: 'true' }
    if (userId) {
      params.user_id = userId
    }
    return await fetchSites(params)
  }

  return {
    loading,
    error,
    fetchSites,
    fetchMejorPuntuados,
    fetchRecientementeAgregados,
    fetchFavoritos
  }
}

