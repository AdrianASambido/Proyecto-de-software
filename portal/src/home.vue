<script setup>
import Carrusel from '@/components/pantalla_inicial/carruselImagenes.vue';
import galeriaTarjetasMonumentos from '@/components/pantalla_inicial/galeriaTarjetasMonumentos.vue';
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/axios.js';

const route = useRoute();
const searchTerm = ref(route.query.search || '');

// 1. Estado para los datos del Carrusel A
const carruselMejorPuntuados = ref([]);

// 2. Estado para los datos del Carrusel B
const carruselRecientementeAgregados = ref([]);

// 3. Estado para los datos de la grilla de tarjetas de monumentos 
const galeriaTarjetasSitios = ref([]);

const filteredSites = computed(() => {
  if (!searchTerm.value) {
    return galeriaTarjetasSitios.value;
  }
  return galeriaTarjetasSitios.value.filter(site =>
    site.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

watch(() => route.query.search, (newSearchTerm) => {
  searchTerm.value = newSearchTerm || '';
});

onMounted(async () => {
  try {
    // Carrusel A (Puntuados)
    const responseMejorPuntuados = await api.get('/sites?order=mejores_puntuados&include_cover=True');
    carruselMejorPuntuados.value = responseMejorPuntuados.data;
    
    // Carrusel B (Recientemente Agregados) 
    const responseRecientementeAgregados = await api.get('/sites?order=fecha=desc&include_cover=True');
    carruselRecientementeAgregados.value = responseRecientementeAgregados.data;

    // galeria tarjetas 
    const responseSitios = await api.get('/sites');
    galeriaTarjetasSitios.value = responseSitios.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
</script>

<template>
  <h1>Página de Inicio</h1>
  
  <Carrusel 
    :items="carruselMejorPuntuados" 
    title="Mejor puntuados"
  />

  <Carrusel 
    :items="carruselRecientementeAgregados" 
    title="Recientemente agregados"
  />

  <galeriaTarjetasMonumentos
    :items="filteredSites"
    title="Sitios Históricos"
  />
</template>
