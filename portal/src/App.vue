<script setup>
import { useRouter } from 'vue-router';
// Importo los componentes desde su nueva ubicación
import HeaderBarraBusqueda from './components/pantalla_inicial//headerBarraBusqueda.vue';
import CarruselImagenes from './components/pantalla_inicial/carruselImagenes.vue';
import HeroPrincipal from './components/pantalla_inicial/heroPrincipal.vue';
import GaleriaTarjetasMonumentos from './components/pantalla_inicial/galeriaTarjetasMonumentos.vue';
import CarruselFavoritos from './components/pantalla_inicial/carruselFavoritos.vue';
import CarruselRecientementeAgregados from './components/pantalla_inicial/carruselRecientementeAgregados.vue';
import Footer from './components/pantalla_inicial/Footer.vue';

const router = useRouter();

const handleSearch = (searchTerm) => {
  router.push({ path: '/', query: { search: searchTerm } });
};
</script>
<template>
  <HeaderBarraBusqueda @search="handleSearch" />
  <!-- Esto está bien ubicado SI-->
  <main>
  
    <HeroPrincipal />
    
    <CarruselImagenes :items="[]" title="Imágenes Destacadas" />
    
    <GaleriaTarjetasMonumentos :items="[]" title="Monumentos Populares" />
    
    <router-view></router-view><!-- renderiza la página constantemente -->
  </main> 
  <Footer />
</template>
<style scoped></style>
