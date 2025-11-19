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
    <div class="main-content">
      <hr class="section-divider" />
      
      <!-- Carrusel principal -->
      <CarruselImagenes 
        title="Imágenes Destacadas"
        :load-params="{ order: 'mejor_puntuado', per_page: 4 }"
      />
      
      <!-- Secciones -->
      <hr class="section-divider" />
      <SeccionMejorPuntuados />
      <hr class="section-divider" />
      <SeccionRecientementeAgregados />
      <hr class="section-divider" />
      <SeccionFavoritos />
    </div>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-divider {
  border: 0;
  height: 3px;
  background-color: rgb(7, 2, 2);  /*#e0e0e0;*/
  margin: 40px 0;
}
</style>
