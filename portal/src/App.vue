<script setup>
// Importo los componentes desde su nueva ubicación
import HeaderBarraBusqueda from './components/pantalla_inicial//headerBarraBusqueda.vue';
import CarruselImagenes from './components/pantalla_inicial/carruselImagenes.vue';
import HeroPrincipal from './components/pantalla_inicial/heroPrincipal.vue';
import GaleriaTarjetasMonumentos from './components/pantalla_inicial/galeriaTarjetasMonumentos.vue';
import CarruselFavoritos from './components/pantalla_inicial/carruselFavoritos.vue';
import CarruselRecientementeAgregados from './components/pantalla_inicial/carruselRecientementeAgregados.vue';


</script>

<template>
  <HeaderBarraBusqueda />
  <!-- Esto está bien ubicado SI-->
  <main>
    <HeroPrincipal />

    <CarruselImagenes /> 
    
    <GaleriaTarjetasMonumentos />
    
    <CarruselFavoritos />

    <CarruselRecientementeAgregados />
    
    <router-view></router-view><!-- renderiza la página constantemente -->
  </main> 
</template>
<style scoped></style>
