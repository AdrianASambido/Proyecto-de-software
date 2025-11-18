<template>
  <section class="container mx-auto p-4 md:p-8 mt-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white shadow-xl rounded-lg overflow-hidden">
      
      <div class="relative h-64 md:h-full">
        <heroCarrusel />
      </div>
      
      <div class="p-6 flex flex-col justify-center items-start">
        <h2 class="text-3xl font-extrabold text-red-700 mb-4"> 
          Ruinas de México
        </h2>
        <p class="text-gray-900 mb-6 leading-relaxed">
          Unas de las estructuras más destacadas de nuestra historia, una reliquia arquitectónica que te llevará de regreso al pasado.
        </p>
        <a href="#" class="
            inline-flex items-center 
            px-4 py-2 border border-portal-red          /* Borde rojo visible por defecto */
            text-sm font-medium rounded-md shadow-sm 
            bg-red-700                               /* Fondo rojo visible por defecto */
            text-white                                  /* Texto blanco visible por defecto */
            
            /* CAMBIO AL PASAR EL RATÓN (HOVER) */
            hover:bg-transparent                        /* Se vuelve transparente al pasar el ratón */
            hover:text-gray-900                         /* El texto se vuelve gris oscuro */
            hover:border-gray-900                       /* El borde se vuelve gris oscuro */
            
            /* Efecto de transición para suavizar el cambio */
            transition-colors duration-200 
            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-portal-red
        ">
            Descubre más
        </a>

      </div>
    </div>
  </section>
</template>

<script setup>
import heroCarrusel from './heroCarrusel.vue';
// Lógica para cargar los datos de la imagen desde una API
</script>

<style scoped>

</style>
