<template>
  <section class="w-full max-w-5xl mx-auto">
    <Swiper
      :modules="[Navigation, Pagination, Autoplay]"
      :slides-per-view="1"
      :space-between="10"
      :loop="true"
      :autoplay="{ delay: 4000, disableOnInteraction: false }"
      navigation
      pagination="{ clickable: true }"
      class="rounded-2xl overflow-hidden shadow-md"
    >
      <SwiperSlide v-for="(img, i) in imagenes" :key="i">
        <img
          :src="img"
          alt="Imagen del sitio"
          class="w-full h-72 sm:h-96 object-cover"
        />
      </SwiperSlide>
    </Swiper>
  </section>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination, Autoplay } from 'swiper/modules'

// ✅ IMPORTANTE: importar estilos de Swiper
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const props = defineProps({
  imagenes: {
    type: Array,
    required: true,
    default: () => []
  }
})
</script>

<style scoped>
.swiper-button-prev,
.swiper-button-next {
  color: white;
  text-shadow: 0 0 6px rgba(0, 0, 0, 0.5);
}

.swiper-pagination-bullet {
  background-color: white;
  opacity: 0.7;
}

.swiper-pagination-bullet-active {
  background-color: #3b82f6; /* azul Tailwind */
  opacity: 1;
}
</style>
