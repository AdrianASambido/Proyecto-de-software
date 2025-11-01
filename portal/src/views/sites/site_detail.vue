<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-4">
    <!-- Botón Volver -->
    <div class="w-full max-w-5xl mb-6">
      <button
        @click="goBack"
        class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-md font-medium focus:outline-none flex items-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Volver
      </button>
    </div>

    <!-- 🏷️ Encabezado del sitio -->
    <div class="w-full max-w-5xl mb-6" v-if="site">
      <SiteHeader :site="site" />
    </div>

    <!-- 🖼️ Galería de imágenes -->
    <div class="w-full max-w-5xl mb-8" v-if="site">
      <SiteGallery :imagenes="site.imagenes" />

    </div>

    <!-- Descripción -->
    <SiteDescription v-if="site" :descripcion_completa="site.descripcion_completa" />

   <!-- 🗺️ Bloque del mapa -->
<div class="w-full max-w-5xl bg-white shadow-md rounded-2xl p-4 mt-10">
  <h2 class="text-xl font-semibold mb-4 text-gray-700 border-b pb-2">
    Ubicación en el mapa
  </h2>
  <SiteMap
    v-if="site && site.latitud && site.longitud"
    :latitud="site.latitud"
    :longitud="site.longitud"
    :nombre="site.nombre"
    :descripcion="site.descripcion_breve"
  />
</div>



    <div v-if="loading" class="text-gray-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import SiteHeader from '@/components/sites/SiteHeader.vue'
import SiteGallery from '@/components/sites/SiteGallery.vue'
import SiteDescription from '@/components/sites/SiteDescription.vue'
import SiteMap from '@/components/sites/SiteMap.vue'

const router = useRouter()
const route = useRoute()

const site = ref(null)
const loading = ref(true)
const error = ref(null)

const goBack = () => {
  router.back()
}

onMounted(async () => {
  try {
    const siteId = route.params.id 
    const response = await api.get(`/sites/${siteId}?include_images=True`)

    site.value = response.data
  } catch (err) {
    error.value = 'No se pudo cargar el sitio.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>
