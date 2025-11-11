<template>
  <section class="carrusel-container">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 px-4">{{ title }}</h2>
    
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="mt-4 text-gray-600">Cargando...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 mx-4">
      {{ error }}
    </div>

    <div v-else-if="items.length === 0" class="text-center py-12 bg-gray-50 rounded-lg mx-4">
      <p class="text-gray-600">No hay sitios destacados disponibles</p>
    </div>

    <div v-else class="slide">
      <baseCard 
        v-for="item in items" 
        :key="item.id"
        :item="item"  
        class="carrusel-item"
      /> 
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import baseCard from '../baseCard.vue';
import { useSites } from '@/composables/useSites';

const props = defineProps({
  // 'items' puede venir como prop o cargarse internamente
  items: {
    type: Array,
    default: () => null // null significa que debe cargarse internamente
  },
  // 'title' es un título opcional para la sección
  title: {
    type: String,
    default: 'Elementos Destacados'
  },
  // Si debe cargar datos automáticamente
  autoLoad: {
    type: Boolean,
    default: true
  },
  // Parámetros para la carga de datos
  loadParams: {
    type: Object,
    default: () => ({ order: 'mejor_puntuado', per_page: 6 })
  }
});

const { loading, error, fetchSites } = useSites();
const internalItems = ref([]);

const loadData = async () => {
  if (props.items !== null) {
    // Si se pasan items como prop, no cargar
    return;
  }
  
  if (loading.value || internalItems.value.length > 0) return;
  
  const data = await fetchSites(props.loadParams);
  internalItems.value = data;
};

const items = computed(() => {
  return props.items !== null ? props.items : internalItems.value;
});

onMounted(() => {
  if (props.autoLoad && props.items === null) {
    loadData();
  }
});
</script>

<style scoped>
.carrusel-container {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 1rem;
}

.slide {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 1rem;
  scroll-behavior: smooth;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.slide::-webkit-scrollbar {
  height: 8px;
}

.slide::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 10px;
}

.slide::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 10px;
}

.slide::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

.carrusel-item {
  flex: 0 0 300px;
  min-width: 300px;
  transition: transform 0.3s ease;
}

.carrusel-item:hover {
  transform: translateY(-5px);
}

@media (max-width: 768px) {
  .carrusel-item {
    flex: 0 0 250px;
    min-width: 250px;
  }
}
</style>
