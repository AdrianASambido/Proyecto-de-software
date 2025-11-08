<template>
  <router-link 
    :to="`/sitio/${item.id}`" 
    class="block max-w-sm rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 bg-white"
  >
    <!-- Imagen de portada -->
    <div class="relative h-48 bg-gray-200 overflow-hidden">
      <img 
        v-if="item.cover_url" 
        :src="item.cover_url" 
        :alt="item.nombre"
        class="w-full h-full object-cover"
      />
      <div v-else class="w-full h-full flex items-center justify-center bg-gray-300">
        <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    </div>

    <!-- Contenido -->
    <div class="p-4">
      <!-- Nombre -->
      <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
        {{ item.nombre }}
      </h3>

      <!-- Ciudad y Provincia -->
      <p class="text-sm text-gray-600 mb-2 flex items-center">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0L6.343 16.657a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        {{ item.ciudad }}, {{ item.provincia }}
      </p>

      <!-- Calificación (si aplica) -->
      <div v-if="formattedRating" class="flex items-center gap-1 text-sm">
        <svg class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span class="text-gray-700 font-semibold">{{ formattedRating }}</span>
        <span class="text-gray-500 text-xs">({{ item.cantidad_resenias || 0 }})</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';
import { defineProps } from 'vue';

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
});

const formattedRating = computed(() => {
  const rating = props.item.valoracion_promedio;
  if (rating == null || rating === undefined || rating === '') {
    return null;
  }
  const numRating = typeof rating === 'number' ? rating : parseFloat(rating);
  if (isNaN(numRating)) {
    return null;
  }
  return numRating.toFixed(1);
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
