<script setup>
import Carrusel from '@/components/pantalla_inicial/carruselImagenes.vue';
import galeriaTarjetasMonumentos from '@/components/pantalla_inicial/galeriaTarjetasMonumentos.vue';
import { ref, onMounted } from 'vue';

import api from '@/api/axios.js';

// 1. Estado para los datos del Carrusel A
const carruselMejorPuntuados = ref([]);

// 2. Estado para los datos del Carrusel B
const carruselRecientementeAgregados = ref([]);

// 3. Estado para los datos de la grilla de tarjetas de monumentos 
const galeriaTarjetasSitios = ref([]);

onMounted(async () => {
  try {
    // Carrusel A (Puntuados)
    const responseMejorPuntuados = await api.get('/sites/best-rated');
    carruselMejorPuntuados.value = responseMejorPuntuados.data;
    
    // Carrusel B (Recientemente Agregados) 
    const responseRecientementeAgregados = await api.get('/sites/recently-added');
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
    :items="galeriaTarjetasSitios"
    title="Sitios Históricos"
  />
</template>
