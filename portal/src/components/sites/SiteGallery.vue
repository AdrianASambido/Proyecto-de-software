<template>
  <div class="bg-white rounded-2xl shadow-md overflow-hidden">
    <swiper
      aria-roledescription="Carrusel de imágenes"
      :modules="[Navigation, Pagination]"
      :slides-per-view="1"
      :loop="true"
      navigation
      pagination
      class="w-full aspect-video"
    >
      <swiper-slide
        v-for="img in imagenes"
        :key="img.id"
        class="flex items-center justify-center"
      >
        <img
          :src="img.url"
          :alt="img.description || 'Imagen del sitio'"
          class="w-full h-full object-cover"
          loading="lazy"
        />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

defineProps({
  imagenes: { type: Array, required: true }
})
</script>

<style scoped>
/* Asegura que el Swiper y las slides llenen completamente el contenedor */
.swiper,
.swiper-slide {
  width: 100%;
  height: 100%;
}

/* Mejora los botones de navegación */
.swiper-button-prev,
.swiper-button-next {
  color: #2563eb; /* azul */
  transition: transform 0.2s ease;
}
.swiper-button-prev:hover,
.swiper-button-next:hover {
  transform: scale(1.2);
}

/* Paginación estética */
.swiper-pagination-bullet {
  background: white;
  opacity: 0.7;
}
.swiper-pagination-bullet-active {
  background: #2563eb;
  opacity: 1;
}
</style>
