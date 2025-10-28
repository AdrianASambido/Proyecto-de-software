<template>
  <section class="carrusel-container">
    <h2>{{ title }}</h2>
    <div class="slide">
      <div v-for="item in items" :key="item.id">
        <img :src="item.src" :alt="item.title">
        <p>{{ item.description }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
// 1. Define las propiedades que el componente espera recibir
const props = defineProps({
  // 'items' es la lista de datos a mostrar (e.g., productos, noticias, fotos)
  
  items: {
    type: Array,
    required: true
  },
  // 'title' es un título opcional para la sección
  title: {
    type: String,
    default: 'Elementos Destacados'
  }
});
</script>

<style scoped>
.carousel-container {
  max-width: 2500px;
  margin: 2rem auto;
  padding: 1rem;
}

.images-wrapper {
  display: flex;
  gap: 1rem;
  overflow: hidden;
  width: 100%;
  justify-content: center;
}

.carousel-item {
  flex: 0 0 calc(33.333% - 1rem);
  transition: transform 0.5s ease;
}

.nav-button {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.nav-button:disabled {
  background-color: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
}
</style>
