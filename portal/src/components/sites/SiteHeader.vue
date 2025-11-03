<template>
  <header class="space-y-3">
    <!-- Encabezado principal: título y favorito -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
      <!-- Nombre y favorito -->
      <div class="flex items-center gap-2">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ site.nombre }}
        </h1>

        <!-- Botón de favorito al lado del nombre (estrella) -->
      <button
  @click="toggleFavorite"
  class="p-2 border rounded-md focus:outline-none transition-colors duration-200"
  :class="isFavorite
    ? 'border-red-400 text-red-400 bg-red-50'
    : 'border-gray-300 text-gray-300 hover:border-gray-400 hover:text-gray-500'"
  :aria-label="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
  :title="isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'"
>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    class="w-5 h-5"
    fill="currentColor"
  >
     <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 
                 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 
                 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 
                 6.86-8.55 11.54L12 21.35z"
            />
  </svg>
</button>


      </div>

      <!-- Rating -->
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
                d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.782 1.401 
                   8.171L12 18.896l-7.335 3.867 1.401-8.171L.132 
                   9.21l8.2-1.192z"
              />
            </svg>
          </template>
        </div>
        <span class="text-sm text-gray-600">
          {{ (site.valoracion_promedio || 0).toFixed(1) }}({{ site.cantidad_resenias || 0 }} reseñas)
        </span>
      </div>
    </div>

    <!-- Línea divisoria -->
    <hr class="border-gray-200" />
    <div class="mt-2 flex gap-2">
      <a 
        v-for="(tag, index) in site.tags" 
        :key="index" 
        :href="`/sitios?tag=${tag}`" 
        class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200"
      >
        {{ tag }}
      </a>
    </div>

    <!-- Detalles secundarios -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-sm text-gray-700">
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
  </header>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  site: {
    type: Object,
    required: true,
    default: () => ({
      nombre: '',
      ciudad: '',
      provincia: '',
      estado_conservacion: 'Bueno',
      valoracion_promedio: 0,
      cantidad_resenias: 0
    })
  }
})

const emit = defineEmits(['update:favorite'])
const isFavorite = ref(false)

const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value
  emit('update:favorite', isFavorite.value)
}

const statusColor = (status) => {
  switch (status) {
    case 'Bueno':
      return 'bg-blue-100 text-blue-800'
    case 'Regular':
      return 'bg-yellow-100 text-yellow-800'
    case 'Malo':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}
</script>

<style scoped>
svg {
  transition: color 0.2s ease;
}
</style>
