<template>
  <div class="max-w-sm rounded overflow-hidden shadow-lg">
    <img class="w-full" :src="item.imagen" :alt="item.nombre">
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">{{ item.nombre }}</div>
      <p class="text-gray-700 text-base">
        {{ item.ciudad }}, {{ item.provincia }}
      </p>
    </div>
    <div class="px-6 pt-4 pb-2">
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">Calificación: {{ item.calificacion }}</span>
      <a :href="item.ubicacion" target="_blank" class="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Ubicación</a>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
});
</script>
