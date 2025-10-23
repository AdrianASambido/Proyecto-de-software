<script setup>
// Importo los componentes desde su nueva ubicación
// preguntar si esto está bien ????
// acá van los import....
import HeaderBarraBusqueda from './components/pantalla_inicial//headerBarraBusqueda.vue';
import CarruselImagenes from './components/pantalla_inicial/carruselImagenes.vue';

</script>

<template>
  <HeaderBarraBusqueda />
  <!-- Esto está bien ubicado -->
  <main>
    <CarruselImagenes /> 
    <router-view></router-view><!-- renderiza la página constantemente -->
  </main> 
</template>
<style scoped></style>
