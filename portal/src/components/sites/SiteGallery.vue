<template>
<<<<<<< HEAD
  <section class="w-full max-w-4xl mx-auto">
    <Swiper
      :modules="[Navigation, Pagination]"
      :slides-per-view="1"
      :loop="true"
      :space-between="20"
      navigation
      :pagination="{ clickable: true }"
      class="rounded-2xl overflow-hidden shadow-lg bg-white/5 backdrop-blur-lg"
    >
      <SwiperSlide v-for="(img, i) in imagenes" :key="img.id || i">
        <div class="relative group">
          <img
            :src="img.url"
            :alt="img.title || 'Imagen del sitio'"
            class="w-full h-60 sm:h-72 md:h-80 object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <!-- Overlay con título -->
          <div
            v-if="img.title"
            class="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/60 to-transparent text-white text-center py-2 text-sm sm:text-base"
          >
            {{ img.title }}
          </div>
        </div>
=======
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
>>>>>>> dev
      </SwiperSlide>
    </Swiper>
  </section>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination, Autoplay } from 'swiper/modules'

<<<<<<< HEAD
// Estilos de Swiper
=======
// ✅ IMPORTANTE: importar estilos de Swiper
>>>>>>> dev
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
<<<<<<< HEAD
  transform: scale(1.3);
}

/* 📐 Ajuste visual de la galería */
.swiper {
  padding-bottom: 1.5rem; /* espacio para las bolitas */
=======
>>>>>>> dev
}
</style>
