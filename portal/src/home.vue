<script setup>
import HeroPrincipal from '@/components/pantalla_inicial/heroPrincipal.vue';
import SeccionMejorPuntuados from '@/components/pantalla_inicial/SeccionMejorPuntuados.vue';
import SeccionRecientementeAgregados from '@/components/pantalla_inicial/SeccionRecientementeAgregados.vue';
import SeccionFavoritos from '@/components/pantalla_inicial/SeccionFavoritos.vue';
import CarruselImagenes from '@/components/pantalla_inicial/carruselImagenes.vue';
</script>

<template>
  <div class="home-page">
    <!-- Hero principal solo visible en Home -->
    <HeroPrincipal />

    <!-- Carrusel principal -->
    <CarruselImagenes 
      title="Imágenes Destacadas"
      :load-params="{ order: 'mejor_puntuado', per_page: 6 }"
    />

    <!-- Secciones -->
    <SeccionMejorPuntuados />
    <SeccionRecientementeAgregados />
    <SeccionFavoritos />
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}
</style>
