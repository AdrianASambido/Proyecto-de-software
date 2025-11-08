<script setup>
import SeccionMejorPuntuados from '@/components/pantalla_inicial/SeccionMejorPuntuados.vue';
import SeccionRecientementeAgregados from '@/components/pantalla_inicial/SeccionRecientementeAgregados.vue';
import SeccionFavoritos from '@/components/pantalla_inicial/SeccionFavoritos.vue';
import CarruselImagenes from '@/components/pantalla_inicial/carruselImagenes.vue';
</script>

<template>
  <div class="home-page">
    <!-- Carrusel de imágenes destacadas -->
    <CarruselImagenes 
      title="Imágenes Destacadas"
      :load-params="{ order: 'mejor_puntuado', per_page: 6 }"
    />
    
    <!-- Sección de Mejor Puntuados con carga perezosa -->
    <SeccionMejorPuntuados />
    
    <!-- Sección de Recientemente Agregados con carga perezosa -->
    <SeccionRecientementeAgregados />
    
    <!-- Sección de Favoritos (solo visible si hay sesión) -->
    <SeccionFavoritos />
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}
</style>
