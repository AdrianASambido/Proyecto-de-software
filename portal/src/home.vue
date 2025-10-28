<script setup>
import Carrusel from '../components/carruselImagenes.vue';
import { ref, onMounted } from 'vue';

// 1. Estado para los datos del Carrusel A
const carruselMejorPuntuados = ref([]);

// 2. Estado para los datos del Carrusel B
const carruselRecientementeAgregados = ref([]);

onMounted(async () => {
  // Cargar datos desde una API
  // Carrusel A (Puntuados)
  //carruselMejorPuntuados.value = await fetch('/api/mejor/Puntuados').then(res => res.json());
  carruselMejorPuntuados.value = await fetch('/api/mejorPuntuados').then(res => res.json());
  
  // Carrusel B (Recientemente Agregados) 
  carruselRecientementeAgregados.value = await fetch('/api/recientementeAgregados').then(res => res.json());
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
</template>