<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">Mis Sitios Favoritos</h1>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Cargando sitios favoritos...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        {{ error }}
      </div>

      <div v-else-if="!sites.length" class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-600 mb-4">No has agregado ningún sitio a tus favoritos todavía.</p>
        <router-link
          to="/sitios"
          class="inline-block px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors"
        >
          Explorar sitios
        </router-link>
      </div>
        <div v-else>
          
          <div class="flex justify-end mb-4">
            <button
              @click="toggleSort"
              class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
            >
              Ordenar: {{ sortOrderLabel }}
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <SiteCard v-for="site in sites" :key="site.id" :site="site" />
          </div>

        </div>

      <div class="mt-8 text-center">
        <router-link
          to="/"
          class="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Volver a la página principal
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import { toast } from 'vue-sonner'
import api from '@/api/axios'
import SiteCard from '@/components/sites/SiteCard.vue'

const sites = ref([])
const loading = ref(true)
const error = ref(null)
const sortOrder = ref('fecha_desc') // desc = más recientes


onMounted(() => {
  console.log('Componente montado')
  loadFavoriteSites()
})

const sortOrderLabel = computed(() =>
  sortOrder.value === 'fecha_desc' ? 'Más recientes' : 'Más antiguos'
)
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'fecha_desc' ? 'fecha_asc' : 'fecha_desc'
  loadFavoriteSites()
}

const loadFavoriteSites = async () => {
  loading.value = true
  error.value = null
  try {
    const params = { order: sortOrder.value }
   
    const { data } = await api.get('/me/favorites', { params })
    sites.value = data.data
  } catch (err) {
 
    error.value = 'No se pudieron cargar tus sitios favoritos.'
    toast.error('Error al cargar los sitios favoritos')
  } finally {
    loading.value = false
  }
}




</script>

<style scoped>
h1 {
  color: #333;
}
</style>
