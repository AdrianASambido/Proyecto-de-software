<template>
  <section class="container mx-auto p-4 md:p-8 mt-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-800">
        {{ title }} 
      </h2>
      <router-link
        v-if="viewAllRoute"
        :to="viewAllRoute"
        class="text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2 transition-colors"
      >
        Ver todos
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </router-link>
    </div>
    
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">Cargando...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
      {{ error }}
    </div>

    <div v-else-if="items.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
      <p class="text-gray-600">{{ emptyMessage || 'No hay sitios disponibles' }}</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <baseCard 
        v-for="item in items" 
        :key="item.id"
        :item="item"  
      /> 
    </div>
  </section>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';
import baseCard from '../baseCard.vue'; 

const router = useRouter();

// DEFINIMOS las Props para que reciba los datos desde el componente padre (Home.vue)
const props = defineProps({
  // Esta prop recibirá el array de objetos (de home.vue)
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  // Esta prop recibirá el título de la sección
  title: {
    type: String,
    default: 'Galería de monumentos'
  },
  // Ruta para "Ver todos" con query params opcionales
  viewAllRoute: {
    type: Object,
    default: null
  },
  // Estado de carga
  loading: {
    type: Boolean,
    default: false
  },
  // Mensaje de error
  error: {
    type: String,
    default: null
  },
  // Mensaje cuando no hay items
  emptyMessage: {
    type: String,
    default: null
  }
});
</script>
