<template>
  <div class="carousel-container">
    <h1 class="text-2xl font-bold mb-4 text-center">Sitios destacados</h1>
    <div class="relative">
      <div class="flex items-center justify-center space-x-4">
        <button @click="prev" :disabled="currentIndex === 0" class="nav-button">
          &lt;
        </button>
        
        <div class="images-wrapper">
          <div v-for="image in visibleImages" :key="image.id" class="carousel-item">
            <img :src="image.src" :alt="image.alt" class="w-full h-full object-cover rounded-lg shadow-md" />
          </div>
        </div>

        <button @click="next" :disabled="currentIndex >= images.length - 3" class="nav-button">
          &gt;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const images = ref([
/** acá van la imagenes del carrusel*/
]);

const currentIndex = ref(0);

const visibleImages = computed(() => {
  return images.value.slice(currentIndex.value, currentIndex.value + 3);
});

const next = () => {
  if (currentIndex.value < images.value.length - 3) {
    currentIndex.value += 3;
  }
};

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 3;
  }
};
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
