<template>
  <div class="bg-white rounded-2xl shadow-md overflow-hidden">
    <swiper
      :modules="[Navigation, Pagination ]"
      :slides-per-view="1"
      :loop="true"
     
      navigation
      pagination
      class="aspect-video"
    >
      <swiper-slide v-for="img in imagenes" :key="img.id">
        <img
          :src="img.url"
          :alt="img.descripcion"
          class="w-full h-full object-cover"
          loading="lazy"
        />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination, Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

defineProps({
  imagenes: { type: Array, required: true }
})
</script>
