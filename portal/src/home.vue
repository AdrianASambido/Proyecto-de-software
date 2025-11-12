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
    <hr class="section-divider" />
    <!-- Carrusel principal -->
    <CarruselImagenes 
      title="Imágenes Destacadas"
      :load-params="{ order: 'mejor_puntuado', per_page: 5 }"
    />
    
    <!-- Secciones -->
    <hr class="section-divider" />
    <SeccionMejorPuntuados />
    <hr class="section-divider" />
    <SeccionRecientementeAgregados />
    <hr class="section-divider" />
    <SeccionFavoritos />
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}

.section-divider {
  border: 0;
  height: 3px;
  background-color: #e0e0e0;
  margin: 40px 0;
}
</style>
