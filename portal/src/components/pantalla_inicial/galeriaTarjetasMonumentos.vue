<template>
  <section class="container mx-auto p-4 md:p-8 mt-8">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
      {{ title }} 
    </h2>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <baseCard 
        v-for="item in items" 
        :key="item.id"
        :item="item"  
      /> 
    </div>
  </section>
</template>

<script setup>
import { defineProps } from 'vue';
import baseCard from '../baseCard.vue'; 

// DEFINIMOS las Props para que reciba los datos desde el componente padre (Home.vue)
const props = defineProps({
  // Esta prop recibirá el array de objetos (de home.vue)
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  // Esta prop recibirá el título de la sección
  title: {
    type: String,
    default: 'Galería de monumentos'
  }
});

// El componente solo muestra lo que le pasemos por 'items'.
</script>
