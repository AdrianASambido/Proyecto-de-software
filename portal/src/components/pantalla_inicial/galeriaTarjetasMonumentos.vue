<template>
  <section class="container mx-auto p-4 md:p-8 mt-8">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
      Monumentos Históricos
    </h2>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <div v-for="monumento in monumentos" :key="monumento.id" class="bg-white rounded-lg shadow-lg overflow-hidden transition-shadow duration-300 hover:shadow-2xl">
        <img 
          :src="monumento.src" 
          :alt="monumento.title" 
          class="w-full h-48 object-cover"
        />
        <div class="p-4">
          <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ monumento.title }}</h3>
          <p class="text-sm text-gray-600">{{ monumento.description }}</p>
        </div>
      </div>
      </div>
  </section>
</template>

<script setup>
// Lógica con datos de ejemplo para la galería
const monumentos = [
    { id: 1, src: 'https://picsum.photos/seed/1/300/200', title: 'Monumento A', description: 'Un sitio con gran valor histórico y arquitectónico.' },
    { id: 2, src: 'https://picsum.photos/seed/11/300/200', title: 'Monumento B', description: 'Ideal para visitar y aprender sobre la cultura local.' },
    { id: 3, src: 'https://picsum.photos/seed/8/300/200', title: 'Monumento C', description: 'Con vistas impresionantes y un diseño único.' },
    { id: 4, src: 'https://picsum.photos/seed/12/300/200', title: 'Monumento D', description: 'Descubre los detalles de su construcción a lo largo del tiempo.' },
    { id: 5, src: 'https://picsum.photos/seed/1/300/200', title: 'Monumento A', description: 'Un sitio con gran valor histórico y arquitectónico.' },
    { id: 6, src: 'https://picsum.photos/seed/11/300/200', title: 'Monumento B', description: 'Ideal para visitar y aprender sobre la cultura local.' },
    { id: 7, src: 'https://picsum.photos/seed/8/300/200', title: 'Monumento C', description: 'Con vistas impresionantes y un diseño único.' },
    { id: 8, src: 'https://picsum.photos/seed/12/300/200', title: 'Monumento D', description: 'Descubre los detalles de su construcción a lo largo del tiempo.' },
];
</script>