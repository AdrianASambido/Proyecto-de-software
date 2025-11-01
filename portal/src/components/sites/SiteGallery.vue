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
/* 🎨 Botones de navegación (modernos, redondos, con efecto hover) */
.swiper-button-prev,
.swiper-button-next {
  color: #fff;
  background-color: rgba(0, 0, 0, 0.4);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.swiper-button-prev:hover,
.swiper-button-next:hover {
  background-color: #3b82f6; /* Azul moderno Tailwind */
  color: white;
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.6);
}

/* 🔵 Paginación moderna */
.swiper-pagination-bullet {
  background-color: #d1d5db; /* gris suave */
  opacity: 0.7;
  transition: all 0.3s ease;
}

.swiper-pagination-bullet-active {
  background-color: #3b82f6; /* azul Tailwind */
  opacity: 1;
}
</style>
