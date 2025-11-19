<template>
  <div class="carousel-container">
    <transition-group name="fade" tag="div">
      <div v-for="(image, index) in images" :key="image.id">
        <img v-if="index === currentIndex" :src="image.src" :alt="image.alt" class="carousel-image" />
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import api from '@/api/axios';

const images = ref([]);
const currentIndex = ref(0);
let intervalId;

const fetchImages = async () => {
  try {
    const response = await api.get('/sites?per_page=6&include_cover=true');
    images.value = response.data.data
      .filter(site => site.cover_url)
      .map(site => ({
        id: site.id,
        src: site.cover_url,
        alt: site.nombre,
      }));
  } catch (error) {
    console.error('Error fetching images:', error);
  }
};

const nextImage = () => {
  if (images.value.length > 0) {
    currentIndex.value = (currentIndex.value + 1) % images.value.length;
  }
};

onMounted(() => {
  fetchImages();
  intervalId = setInterval(nextImage, 6000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  clip-path: polygon(5% 0, 95% 0, 100% 100%, 0 100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
