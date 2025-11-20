<template>
  <div ref="galleryEl" class="bg-white rounded-2xl shadow-md overflow-hidden relative">
      <swiper
      aria-roledescription="Carrusel de imágenes"
      :modules="[Navigation, Pagination, Keyboard]"
      :slides-per-view="1"
      :loop="true"
      :navigation="{ prevEl: '.gallery-nav-prev', nextEl: '.gallery-nav-next' }"
      :keyboard="{ enabled: true }"
      pagination
      class="w-full relative"
    >
   <swiper-slide
  v-for="(img, index) in orderedImages"
  :key="img.id || index"
  class="flex items-center justify-center"
>
  <div class="w-full h-full bg-gray-100 flex items-center justify-center overflow-hidden gallery-slide-container">
    <img
      :src="img.url"
      :alt="img.description || 'Imagen del sitio'"
      :class="['w-full h-full object-fill select-none gallery-img', { loaded: loaded[index] }]"
      loading="lazy"
      decoding="async"
      draggable="false"
      width="1200"
      height="675"
      style="object-position: center; max-width: none;"
      @load="onImgLoad(index)"
    />
  </div>
</swiper-slide>
    </swiper>

    <button ref="prevBtn" class="gallery-nav-prev" aria-label="Anterior">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <button ref="nextBtn" class="gallery-nav-next" aria-label="Siguiente">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 6L15 12L9 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>
<script setup>
import { computed, ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination, Keyboard } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const props = defineProps({
  imagenes: { type: Array, required: true }
})


const loaded = ref([])

const onImgLoad = (index) => {
  loaded.value[index] = true
  updateNavPositions()
}

watch(() => props.imagenes, (imgs) => {
  loaded.value = (imgs || []).map(() => false)
}, { immediate: true })


const orderedImages = computed(() => {
  if (!props.imagenes) return []

  const portada = props.imagenes.find(i => i.is_cover)
  const resto = props.imagenes
    .filter(i => i !== portada)
    .sort((a, b) => (a.order || 0) - (b.order || 0))

  return portada ? [portada, ...resto] : resto
})

const galleryEl = ref(null)
const prevBtn = ref(null)
const nextBtn = ref(null)

function updateNavPositions() {
  return
}

let resizeObserver = null
onMounted(async () => {
  await nextTick()
  updateNavPositions()
  window.addEventListener('resize', updateNavPositions)
  try {
    resizeObserver = new ResizeObserver(() => updateNavPositions())
    if (galleryEl.value) resizeObserver.observe(galleryEl.value)
  } catch (e) {}
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateNavPositions)
  if (resizeObserver && galleryEl.value) resizeObserver.unobserve(galleryEl.value)
})
</script>


<style scoped>

.swiper,
.swiper-slide {
  width: 100%;
  height: 100%;
}


.swiper-button-prev,
.swiper-button-next {
  color: #374151;
  background: rgba(255,255,255,0.85);
  border-radius: 9999px;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  opacity: 0.85;
  transition: transform 0.15s ease, opacity 0.15s ease;
}
.swiper-button-prev:hover,
.swiper-button-next:hover {
  transform: scale(1.05);
  opacity: 1;
}


.swiper-pagination-bullet {
  background: white;
  opacity: 0.7;
}
.swiper-pagination-bullet-active {
  background: #374151;
  opacity: 1;
}


.swiper-button-prev,
.swiper-button-next {
  display: none !important;
}


.gallery-nav-prev,
.gallery-nav-next {
  position: absolute;
  top: 50%;
  z-index: 30;
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  background: rgba(255,255,255,0.85);
  color: #111827;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 18px rgba(17,24,39,0.06);
  border: 1px solid rgba(17,24,39,0.06);
  transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease, background 0.12s ease;
  opacity: 0.95;
}
.gallery-nav-prev { left: 1rem; transform: translateY(-50%); width: 3.25rem; height: 3.25rem; padding: 0.25rem; }
.gallery-nav-next { right: 1rem; transform: translateY(-50%); width: 3.25rem; height: 3.25rem; padding: 0.25rem; }
.gallery-nav-prev:hover,
.gallery-nav-next:hover {
  transform: translateY(-50%) scale(1.06);
  box-shadow: 0 12px 36px rgba(17,24,39,0.12);
  opacity: 1;
  background: rgba(17,24,39,0.06);
  color: #0f172a; 
}


.gallery-nav-prev:focus,
.gallery-nav-next:focus {
  outline: 3px solid rgba(59,130,246,0.12);
  outline-offset: 3px;
  opacity: 1;
}

@media (max-width: 640px) {
  .gallery-nav-prev,
  .gallery-nav-next {
    width: 2.5rem;
    height: 2.5rem;
    transform: translateY(-50%); 
    padding: 0.2rem;
  }

  .gallery-nav-prev {
    left: 0.5rem;
  }

  .gallery-nav-next {
    right: 0.5rem;
  }


  .gallery-nav-prev svg,
  .gallery-nav-next svg {
    width: 16px;
    height: 16px;
  }
}


.gallery-nav-prev:focus,
.gallery-nav-next:focus {
  outline: 2px solid rgba(59,130,246,0.15);
  outline-offset: 2px;
}


.gallery-img {
  opacity: 0;
  transition: opacity 320ms ease-in-out, transform 320ms ease-in-out;
  transform: scale(1.01);
}
.gallery-img.loaded {
  opacity: 1;
  transform: scale(1);
}


  .gallery-slide-container {
    aspect-ratio: 16/9;
    overflow: hidden;
  }

  @media (min-width: 768px) {

  .gallery-slide-container {
    aspect-ratio: auto;
    height: 420px;
    padding-top: 0; 
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .gallery-img {
    object-fit: fill;
    width: 100%;
    height: 100%;
  }
}
</style>
