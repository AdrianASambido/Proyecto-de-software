<template>
  <header class="space-y-3 px-2 sm:px-0">
    <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
      <div class="flex-1">
        <div class="flex items-center gap-3">
          <h1 class="text-3xl font-bold text-gray-900 leading-tight">
            {{ site.nombre }}
          </h1>

        
        </div>

        <div class="mt-2 flex items-center gap-4">
          <div class="flex items-center gap-2">
           <div class="flex items-center -ml-1">
            <template v-for="n in 5" :key="n">
              <svg
                class="w-5 h-5"
                viewBox="0 0 20 20"
                :class="n <= Math.round(ratingValue)
                  ? 'fill-yellow-400'
                  : 'fill-gray-300'"
              >
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
                />
              </svg>
            </template>
</div>

           <span class="text-sm text-gray-600">
  <template v-if="reviewsCount > 0">
    {{ ratingValue.toFixed(1) }} · {{ reviewsCount }} reseñas
  </template>
  <template v-else>
    0.0 · 0 reseñas
  </template>
</span>

          </div>

         

            <!-- ubicación movida abajo en el bloque de metadatos para evitar duplicados -->
        </div>
      </div>

      <div class="flex items-center gap-2 mt-2 sm:mt-0">
        <button
          @click="toggleFavorite"
          class="px-3 py-2 border rounded-md focus:outline-none transition-all duration-200 flex items-center gap-2"
          :class="isFavorite ? 'border-red-400 text-red-500 bg-red-50' : 'border-gray-300 text-gray-700 hover:border-gray-400'"
          :aria-label="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
          :disabled="loading"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
          <span class="text-sm">{{ isFavorite ? 'Favorito' : 'Agregar' }}</span>
        </button>

    
      </div>
    </div>

    <hr class="border-gray-200" />

  
<div
  v-if="site.tags && site.tags.length > 0"
  class="mt-2 flex flex-wrap gap-2"
>
  <!-- Tags visibles -->
  <button
    v-for="tag in visibleTags"
    :key="tag.id"
    :title="tag.nombre"
    @click="goToTag(tag)"
    class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200 transition max-w-xs truncate"
  >
    {{ tag.nombre }}
  </button>

  <!-- Botón Ver más / Ver menos -->
  <button
    v-if="site.tags.length > 5"
    @click="showAllTags = !showAllTags"
    class="inline-flex items-center px-2 py-1 bg-gray-200 text-gray-800 rounded-full text-sm hover:bg-gray-300 transition"
  >
    {{ showAllTags ? 'Ver menos' : `+${site.tags.length - 5} más` }}
  </button>
</div>


<div class="grid grid-cols-1 gap-3 text-sm text-gray-700 mt-2">
  <div>
    <span class="font-semibold text-gray-900">Ubicado en :</span>
    <span>{{ site.ciudad }}, {{ site.provincia }}</span>
  </div>

  <div>
    <span class="font-semibold text-gray-900">Estado de conservación:</span>
    <span
      class="ml-2 inline-block px-3 py-1 rounded-full text-xs font-semibold"
      :class="statusColor(site.estado_conservacion)"
    >
      {{ site.estado_conservacion }}
    </span>
  </div>

  <div v-if="site.inauguracion">
    <span class="font-semibold text-gray-900">Inaugurado en :</span>
    <span>{{ site.inauguracion }}</span>
  </div>
</div>

 <LoginPopup
  v-model="showLoginPopup"
  @login="onLoginSuccess"
/>



  </header>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'

import api from '@/api/axios' 
const props = defineProps({
  site: { type: Object, required: true },
  userId: { type: Number, required: true },
 
})
import LoginPopup from '@/components/login_google/loginPopUp.vue'


import { useRouter } from 'vue-router'
const router = useRouter()

const goToTag = (tag) => {
 
  if (!tag?.id) return
  router.push({ path: '/sitios', query: { tags: tag.id } })
}

const emit = defineEmits(['update:favorite'])
const isFavorite = ref(false)
const loading = ref(false)
const showLoginPopup = ref(false)
const checkFavorite = async () => {
  if (!props.site?.id) return
  try {
    if (!props.userId) {
      isFavorite.value = false
      return
    }
    const res = await api.get(`/sites/${props.site.id}/favorite`, {
      params: { userId: props.userId },
    })
    isFavorite.value = !!res.data.favorite
  } catch (err) {
    console.warn('Error comprobando favorito:', err)
  }
}
const showAllTags = ref(false)

const visibleTags = computed(() =>
  showAllTags.value
    ? props.site.tags
    : props.site.tags.slice(0, 5)
)


onMounted(checkFavorite)
watch(() => props.site?.id, (newId) => { if (newId) checkFavorite() })
const toggleFavorite = async () => {
  if (!props.userId) {
    showLoginPopup.value = true
    return
  }

  if (!props.site?.id) return
  loading.value = true
  const url = `/sites/${props.site.id}/favorite?userId=${props.userId}`

  try {
    if (isFavorite.value) {
      const res = await api.delete(url)
      if ([200, 204].includes(res.status)) isFavorite.value = false
    } else {
      const res = await api.put(url)
      if ([200, 201, 204].includes(res.status)) isFavorite.value = true
    }
    emit('update:favorite', isFavorite.value)
  } catch (error) {
    console.error('Error al actualizar favorito:', error?.response?.data || error.message)
  } finally {
    loading.value = false
  }
}
const onLoginSuccess = (user) => {
  console.log("Usuario logueado:", user)
 
  window.location.reload()
}


const statusColor = (estado) => {
  switch (estado) {
    case 'Bueno': return 'bg-blue-100 text-blue-800'
    case 'Regular': return 'bg-yellow-100 text-yellow-800'
    case 'Malo': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-700'
  }
}

// Computed: normalize rating and reviews count from various possible backend fields
const ratingValue = computed(() => {
  const s = props.site || {}
  const keys = ['valoracion_promedio', 'valoracion', 'rating', 'average_rating', 'promedio_valoracion']

  for (const k of keys) {
    const v = s[k]
    if (v != null && !isNaN(Number(v))) return Number(v)
  }

  if (s.stats && s.stats.average && !isNaN(Number(s.stats.average))) {
    return Number(s.stats.average)
  }

  // Siempre devolver 0 cuando no hay reseñas
  return 0
})


const reviewsCount = computed(() => {
  const s = props.site || {}
  const keys = ['cantidad_resenias', 'cantidad_resenas', 'reviews_count', 'reviewsCount', 'cantidad']
  for (const k of keys) {
    const v = s[k]
    if (Array.isArray(v)) return v.length
    if (v != null && !isNaN(Number(v))) return Number(v)
  }
  if (Array.isArray(s.reviews)) return s.reviews.length
  if (s.reviews_count != null && !isNaN(Number(s.reviews_count))) return Number(s.reviews_count)
  return 0
})


</script>

<style scoped>
svg { transition: color 0.2s ease; }
button[disabled] { opacity: 0.6; cursor: not-allowed; }
</style>
