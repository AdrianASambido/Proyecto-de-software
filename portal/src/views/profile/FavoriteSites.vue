<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4">


      <div class="w-40 mb-6">
        <RouterLink
          to="/"
          class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-700 rounded-lg font-medium shadow-sm border flex items-center gap-2 transition"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver
        </RouterLink>
      </div>

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

        <!-- PAGINACION -->
        <div v-if="meta.total > meta.per_page" class="flex justify-center items-center gap-4 mt-8">
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Anterior
          </button>

          <span class="text-gray-600">
            Página {{ currentPage }} de {{ totalPages }}
          </span>

          <button
            @click="nextPage"
            :disabled="currentPage >= totalPages"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Siguiente
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { toast } from 'vue-sonner'
import api from '@/api/axios'
import SiteCard from '@/components/sites/SiteCard.vue'

const sites = ref([])
const loading = ref(true)
const error = ref(null)
const sortOrder = ref('fecha_desc') // desc = más recientes

// --- PAGINACION ---
const currentPage = ref(1)
const perPage = ref(25) // sitios por página
const meta = ref({ total: 0, per_page: 25 }) // debe coincidir con perPage
const totalPages = computed(() => Math.ceil(meta.value.total / meta.value.per_page))

// --- Carga de sitios ---
const loadFavoriteSites = async (page = 1) => {
  loading.value = true
  error.value = null
  try {
    const params = { 
      order: sortOrder.value,
      page: page,
      per_page: perPage.value
    }
    const { data } = await api.get('/me/favorites', { params })
    sites.value = data.data
    meta.value = data.meta // meta: { total, per_page, page }
    currentPage.value = page
  } catch (err) {
    error.value = 'No se pudieron cargar tus sitios favoritos.'
    toast.error('Error al cargar los sitios favoritos')
  } finally {
    loading.value = false
  }
}

onMounted(() => loadFavoriteSites())

// --- Orden ---
const sortOrderLabel = computed(() =>
  sortOrder.value === 'fecha_desc' ? 'Más recientes' : 'Más antiguos'
)
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'fecha_desc' ? 'fecha_asc' : 'fecha_desc'
  loadFavoriteSites(1)
}

// --- Funciones de paginación ---
const previousPage = () => {
  if (currentPage.value > 1) loadFavoriteSites(currentPage.value - 1)
}
const nextPage = () => {
  if (currentPage.value < totalPages.value) loadFavoriteSites(currentPage.value + 1)
}
</script>

<style scoped>
h1 {
  color: #333;
}
</style>
