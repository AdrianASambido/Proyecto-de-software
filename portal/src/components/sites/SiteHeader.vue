<template>
  <header class="space-y-3">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
      <div class="flex items-center gap-2">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ site.nombre }}
        </h1>

        <button
          @click="toggleFavorite"
          class="p-2 border rounded-md focus:outline-none transition-all duration-200"
          :class="isFavorite
            ? 'border-red-400 text-red-500 bg-red-50 scale-105'
            : 'border-gray-300 text-gray-400 hover:border-gray-400 hover:text-gray-500'"
          :aria-label="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
          :title="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
          :disabled="loading"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            class="w-5 h-5"
            :class="isFavorite ? 'text-red-500' : 'text-gray-300'"
            fill="currentColor"
          >
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09
                 C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42
                 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            />
          </svg>
        </button>
      </div>

     
      <div class="flex items-center space-x-2">
        <div class="flex items-center space-x-1">
          <template v-for="n in 5" :key="n">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              class="w-5 h-5"
              :class="n <= Math.round(site.valoracion_promedio) ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor"
            >
              <path
                d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.782
                   1.401 8.171L12 18.896l-7.335 3.867
                   1.401-8.171L.132 9.21l8.2-1.192z"
              />
            </svg>
          </template>
        </div>
        <span class="text-sm text-gray-600">
          {{ (site.valoracion_promedio || 0).toFixed(1) }} ({{ site.cantidad_resenias || 0 }} reseñas)
        </span>
      </div>
    </div>

    <hr class="border-gray-200" />

  
<div
  class="mt-2 gap-2"
  :class="showAllTags 
      ? 'grid grid-cols-5 auto-rows-min gap-2' 
      : 'flex flex-wrap gap-2'"
>
  <!-- Tags visibles -->
  <button
    v-for="tag in visibleTags"
    :key="tag.id"
    :title="tag.nombre"
    @click="goToTag(tag)"
    class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200 transition w-fit whitespace-nowrap"
  >
    {{ tag.nombre }}
  </button>

  <!-- Botón Ver más / Ver menos -->
  <button
    v-if="site.tags.length > 5"
    @click="showAllTags = !showAllTags"
    class="px-2 py-1 bg-gray-200 text-gray-800 rounded-full text-sm hover:bg-gray-300 transition w-fit whitespace-nowrap"
  >
    {{ showAllTags ? 'Ver menos' : `+${site.tags.length - 5} más` }}
  </button>
</div>



    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-sm text-gray-700 mt-2">
      <div>
        <span class="font-semibold text-gray-900">Ubicación:</span>
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
</script>

<style scoped>
svg { transition: color 0.2s ease; }
button[disabled] { opacity: 0.6; cursor: not-allowed; }
</style>
