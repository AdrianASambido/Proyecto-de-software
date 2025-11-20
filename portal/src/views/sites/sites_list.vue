<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header con búsqueda -->
    <div class="bg-white shadow-sm sticky top-0 z-40">
      <div class="container mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Búsqueda por texto -->
          <div class="flex-1">
            <div class="relative">
              <input
                v-model="filters.busqueda"
                @input="debouncedSearch"
                type="text"
                placeholder="Buscar por nombre o descripción..."
                class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <!-- Botón de filtros (mobile) -->
          <button
            @click="showFilters = !showFilters"
            class="md:hidden px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filtros
            <span v-if="activeFiltersCount > 0" class="bg-white text-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">
              {{ activeFiltersCount }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-6">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Panel de filtros (sidebar en desktop, acordeón en mobile) -->
        <div 
          :class="[
            'lg:w-80 flex-shrink-0',
            showFilters ? 'block' : 'hidden lg:block'
          ]"
        >
          <div class="bg-white rounded-lg shadow-md p-4 sticky top-24">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-800">Filtros</h2>
              <button
                @click="clearFilters"
                class="text-sm text-blue-600 hover:text-blue-800"
              >
                Limpiar
              </button>
            </div>

            <!-- Ciudad -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Ciudad</label>
              <input
                v-model="filters.ciudad"
                @input="debouncedSearch"
                type="text"
                placeholder="Ej: Buenos Aires"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <!-- Provincia -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Provincia</label>
              <select
                v-model="filters.provincia"
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todas las provincias</option>
                <option v-for="prov in provincias" :key="prov.value" :value="prov.value">
                  {{ prov.label }}
                </option>
              </select>
            </div>

            <!-- Estado de conservación -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Estado de conservación</label>
              <select
                v-model="filters.estado_conservacion"
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos</option>
                <option value="Bueno">Bueno</option>
                <option value="Regular">Regular</option>
                <option value="Malo">Malo</option>
              </select>
            </div>

            <!-- Tags -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
              <div class="max-h-40 overflow-y-auto border border-gray-300 rounded-md p-2">
                <label
                  v-for="tag in tags"
                  :key="tag.id"
                  class="flex items-center mb-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
                >
                  <input
                    type="checkbox"
                    :value="tag.id"
                    v-model="filters.tags"
                    @change="applyFilters"
                    class="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">{{ tag.name }}</span>
                </label>
              </div>
            </div>

            <!-- Favoritos -->
            <div class="mb-4">
              <label class="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  v-model="filters.favoritos"
                  @change="handleFavoritosChange"
                  :disabled="!isAuthenticated"
                  class="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <span class="text-sm font-medium text-gray-700">Solo favoritos</span>
              </label>
              <p v-if="!isAuthenticated && filters.favoritos" class="text-xs text-blue-600 mt-1">
                <router-link to="/login" class="underline">Inicia sesión</router-link> para ver tus favoritos
              </p>
            </div>

            <!-- Búsqueda en mapa -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Búsqueda en mapa</label>
              <button
                @click="showMap = !showMap"
                class="w-full px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-sm text-gray-700 flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
                {{ showMap ? 'Ocultar mapa' : 'Ver mapa' }}
              </button>
            </div>

            <!-- Orden -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">Ordenar por</label>
              <select
                v-model="filters.order"
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="fecha_desc">Más recientes</option>
                <option value="fecha_asc">Más antiguos</option>
                <option value="nombre_asc">Nombre (A-Z)</option>
                <option value="nombre_desc">Nombre (Z-A)</option>
                <option value="mejor_puntuado">Mejor puntuados</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Contenido principal -->
        <div class="flex-1">
          <!-- Mapa principal -->
          <div
            v-if="showMap"
            class="mb-6 bg-white rounded-lg shadow border border-gray-200 p-4 space-y-4 relative z-0"
          >
            <div class="space-y-2 sm:flex sm:items-center sm:justify-between sm:space-y-0">
              <h2 class="text-lg font-semibold text-gray-800">Búsqueda geográfica</h2>
              <p class="text-sm text-gray-500 sm:text-right">
                Mueve el mapa o ajusta el zoom y luego presiona “Actualizar Radio de Búsqueda”.
              </p>
            </div>
            <div class="rounded-lg overflow-hidden border border-gray-300 h-64 sm:h-80 lg:h-[34rem]">
              <Map @update-location="handleMapLocationUpdate" />
            </div>
          </div>

          <!-- Resultados -->
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p class="mt-4 text-gray-600">Cargando sitios...</p>
          </div>

          <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {{ error }}
          </div>

          <div v-else>
            <!-- Información de resultados -->
            <div class="mb-4 flex items-center justify-between">
              <p class="text-gray-600">
                Mostrando {{ sites.length }} de {{ total }} sitios
              </p>
            </div>

            <!-- Grid de sitios -->
            <div v-if="sites.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              <SiteCard
                v-for="site in sites"
                :key="site.id"
                :site="site"
              />
            </div>

            <!-- Sin resultados -->
            <div v-else-if="hasLoadedOnce" class="text-center py-12 bg-white rounded-lg shadow-md">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">No se encontraron sitios</h3>
              <p class="mt-1 text-sm text-gray-500">Intenta ajustar tus filtros de búsqueda.</p>
            </div>

            <!-- Paginación -->
            <div v-if="totalPages > 1" class="mt-8 flex justify-center items-center gap-2">
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Anterior
              </button>
              
              <span class="px-4 py-2 text-gray-700">
                Página {{ currentPage }} de {{ totalPages }}
              </span>
              
              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Siguiente
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import SiteCard from '@/components/sites/SiteCard.vue'
import { useAuth } from '@/composables/useAuth'
import Map from '@/views/sites/Map.vue'

const route = useRoute()
const router = useRouter()
const { isAuthenticated, currentUser } = useAuth()

// Estado
const sites = ref([])
const loading = ref(false)
const error = ref(null)
const total = ref(0)
const currentPage = ref(1)
const perPage = 12
const totalPages = computed(() => Math.ceil(total.value / perPage))
const hasLoadedOnce = ref(false)

// Filtros
const filters = ref({
  busqueda: '',
  ciudad: '',
  provincia: '',
  estado_conservacion: '',
  tags: [],
  favoritos: false,
  order: 'fecha_desc',
  latitud: null,
  longitud: null,
  radio: 5
})

const showFilters = ref(false)
const showMap = ref(false)

// Provincias argentinas
const provincias = ref([
  { value: 'Buenos Aires', label: 'Buenos Aires' },
  { value: 'Catamarca', label: 'Catamarca' },
  { value: 'Chaco', label: 'Chaco' },
  { value: 'Chubut', label: 'Chubut' },
  { value: 'Córdoba', label: 'Córdoba' },
  { value: 'Corrientes', label: 'Corrientes' },
  { value: 'Entre Ríos', label: 'Entre Ríos' },
  { value: 'Formosa', label: 'Formosa' },
  { value: 'Jujuy', label: 'Jujuy' },
  { value: 'La Pampa', label: 'La Pampa' },
  { value: 'La Rioja', label: 'La Rioja' },
  { value: 'Mendoza', label: 'Mendoza' },
  { value: 'Misiones', label: 'Misiones' },
  { value: 'Neuquén', label: 'Neuquén' },
  { value: 'Río Negro', label: 'Río Negro' },
  { value: 'Salta', label: 'Salta' },
  { value: 'San Juan', label: 'San Juan' },
  { value: 'San Luis', label: 'San Luis' },
  { value: 'Santa Cruz', label: 'Santa Cruz' },
  { value: 'Santa Fe', label: 'Santa Fe' },
  { value: 'Santiago del Estero', label: 'Santiago del Estero' },
  { value: 'Tierra del Fuego', label: 'Tierra del Fuego' },
  { value: 'Tucumán', label: 'Tucumán' }
])

// Tags
const tags = ref([])

// Contador de filtros activos
const activeFiltersCount = computed(() => {
  let count = 0
  if (filters.value.busqueda) count++
  if (filters.value.ciudad) count++
  if (filters.value.provincia) count++
  if (filters.value.estado_conservacion) count++
  if (filters.value.tags.length > 0) count++
  if (filters.value.favoritos) count++
  if (filters.value.latitud && filters.value.longitud) count++
  return count
})

// Manejar actualización de ubicación desde el mapa
const handleMapLocationUpdate = (location) => {
  filters.value.latitud = location.latitud
  filters.value.longitud = location.longitud
  filters.value.radio = location.radio
  showMap.value = true
  applyFilters()
}

// Debounce para búsqueda
let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 500)
}

// Cargar tags
const loadTags = async () => {
  try {
    const { data } = await api.get('/tags')
    tags.value = data.data || []
  } catch (err) {
    console.error('Error cargando tags:', err)
  }
}

// Cargar sitios
const loadSites = async () => {
  loading.value = true
  error.value = null
  
  try {
    const params = {
      page: currentPage.value,
      per_page: perPage,
      include_cover: 'true'
    }

    // Agregar filtros
    if (filters.value.busqueda) params.busqueda = filters.value.busqueda
    if (filters.value.ciudad) params.ciudad = filters.value.ciudad
    if (filters.value.provincia) params.provincia = filters.value.provincia
    if (filters.value.estado_conservacion) params.estado_conservacion = filters.value.estado_conservacion
    if (filters.value.tags.length > 0) params.tags = filters.value.tags.join(',')
    if (filters.value.order) params.order = filters.value.order
    if (filters.value.latitud && filters.value.longitud) {
      params.latitud = filters.value.latitud
      params.longitud = filters.value.longitud
      params.radio = filters.value.radio || 5
    }
    
    // Si se filtran por favoritos y el usuario está autenticado, usar el endpoint /me/favorites
    // que requiere JWT y obtiene el user_id del token
    let endpoint = '/sites'
    if (filters.value.favoritos && isAuthenticated.value) {
      endpoint = '/me/favorites'
    } else if (filters.value.favoritos && !isAuthenticated.value) {
      // Si se intenta filtrar por favoritos sin autenticación, remover el filtro
      filters.value.favoritos = false
    }
    const { data } = await api.get(endpoint, { params })
    sites.value = data.data || []
    total.value = data.meta?.total || 0
    currentPage.value = data.meta?.page || 1
    hasLoadedOnce.value = true

  } catch (err) {
    console.error('Error cargando sitios:', err)
    error.value = 'Error al cargar los sitios. Por favor, intenta nuevamente.'
    sites.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// Manejar cambio de favoritos
const handleFavoritosChange = () => {
  if (filters.value.favoritos && !isAuthenticated.value) {
    // Si no está autenticado y se intenta activar favoritos, desactivar y redirigir
    filters.value.favoritos = false
    router.push('/login')
    return
  }
  applyFilters()
}

// Aplicar filtros y actualizar URL
const applyFilters = () => {
  currentPage.value = 1
  updateURL()
  loadSites()
}

// Limpiar filtros
const clearFilters = () => {
  filters.value = {
    busqueda: '',
    ciudad: '',
    provincia: '',
    estado_conservacion: '',
    tags: [],
    favoritos: false,
    order: 'fecha_desc',
    latitud: null,
    longitud: null,
    radio: 5
  }
  showMap.value = false
  applyFilters()
}

// Actualizar URL con query params
const updateURL = () => {
  const query = {}
  if (filters.value.busqueda) query.busqueda = filters.value.busqueda
  if (filters.value.ciudad) query.ciudad = filters.value.ciudad
  if (filters.value.provincia) query.provincia = filters.value.provincia
  if (filters.value.estado_conservacion) query.estado_conservacion = filters.value.estado_conservacion
  if (filters.value.tags.length > 0) query.tags = filters.value.tags.join(',')
  if (filters.value.favoritos) query.favoritos = 'true'
  if (filters.value.order && filters.value.order !== 'fecha_desc') query.order = filters.value.order
  if (filters.value.latitud && filters.value.longitud) {
    query.latitud = filters.value.latitud
    query.longitud = filters.value.longitud
    query.radio = filters.value.radio
  }
  if (currentPage.value > 1) query.page = currentPage.value

  router.replace({ query })
}

// Cargar filtros desde URL
const loadFiltersFromURL = () => {
  const query = route.query
  if (query.busqueda) filters.value.busqueda = query.busqueda
  if (query.ciudad) filters.value.ciudad = query.ciudad
  if (query.provincia) filters.value.provincia = query.provincia
  if (query.estado_conservacion) filters.value.estado_conservacion = query.estado_conservacion
  if (query.tags) filters.value.tags = query.tags.split(',').map(t => parseInt(t)).filter(t => !isNaN(t))
  if (query.favoritos === 'true') filters.value.favoritos = true
  if (query.order) filters.value.order = query.order
    if (query.latitud && query.longitud) {
      filters.value.latitud = parseFloat(query.latitud)
      filters.value.longitud = parseFloat(query.longitud)
      filters.value.radio = query.radio ? parseFloat(query.radio) : 5
    }
  if (query.page) currentPage.value = parseInt(query.page) || 1

  if (filters.value.latitud && filters.value.longitud) {
    showMap.value = true
  }
}

// Navegación de páginas
const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  updateURL()
  loadSites()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Lifecycle
onMounted(async () => {
  loadFiltersFromURL()
  await loadTags()
  await loadSites()
  
  // Mostrar filtros en desktop por defecto
  if (window.innerWidth >= 1024) {
    showFilters.value = true
  }
})
</script>
