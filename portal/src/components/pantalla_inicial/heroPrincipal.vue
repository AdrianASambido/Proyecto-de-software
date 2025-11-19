<template>
  <section class="container mx-auto p-4 md:p-8 mt-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white shadow-xl rounded-lg overflow-hidden">

      <div class="relative h-96 md:h-full">

      <div class="relative h-96 md:h-full">
        <heroCarrusel />
      </div>
      
      <div class="p-6 flex flex-col justify-center items-start">
        <h2 class="text-3xl font-extrabold text-red-700 mb-4"> 
          Tu portal de sitios históricos
          Tu portal de sitios históricos
        </h2>
        <div class="text-justify text-gray-900 text-lg font-serif mb-4 leading-relaxed text-intro">

          <p>Donde encontrarás las estructuras más destacadas de nuestra historia, reliquias</p>

          <p class="ml-2"> arquitectónica que te llevarán a un paseo por el pasado.  Aquí podrás obtener </p>

          <p class="ml-4"> información  relevante de los sitios históricos, ver imágenes, elegir las  que </p>

          <p class="ml-6"> más te gusten, calificarlas, ver su ubicación y más.</p>
        </div>
        <router-link to="/sitios" class="inline-flex items-center px-4 py-2 border border-portal-red text-sm font-medium
            rounded-md shadow-sm bg-red-700 text-white hover:bg-transparent hover:text-gray-900
            hover:border-gray-900 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-portal-red
        ">
            Descubre más
        </router-link>
        </router-link>

      </div>
    </div>
  </section>
</template>

<script setup>
import heroCarrusel from './heroCarrusel.vue';

</script>+

</script>+

<style scoped>

.text-intro {
  text-indent: 2em; 
}
.text-intro {
  text-indent: 2em; 
}
</style>
