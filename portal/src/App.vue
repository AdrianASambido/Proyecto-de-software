<script setup>
import { useRouter } from 'vue-router';
import HeaderBarraBusqueda from './components/pantalla_inicial/headerBarraBusqueda.vue';
import HeroPrincipal from './components/pantalla_inicial/heroPrincipal.vue';
import Footer from './components/pantalla_inicial/Footer.vue';

const router = useRouter();

const handleSearch = (searchTerm) => {
  router.push({ path: '/', query: { search: searchTerm } });
};
</script>
<template>
  <HeaderBarraBusqueda @search="handleSearch" />

  <main>
    
   
    <router-view />
  </main>

  <Footer />
</template>

<style scoped></style>
