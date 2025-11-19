<template>
  
  <div class="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4 space-y-10">

    <div class="w-full max-w-5xl">
      <button
        @click="goBack"
        class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-700 rounded-lg font-medium shadow-sm border flex items-center gap-2 transition"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver
      </button>
    </div>

 
    <div class="w-full max-w-5xl">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
       
        <div class="lg:col-span-4">
          <div class="mb-4">
            <SiteHeader v-if="site" :site="site" :user-id="userId" />
          </div>
        </div>


        <div class="lg:col-span-8">
          <SiteGallery v-if="site && site.imagenes?.length" :imagenes="site.imagenes" />
        </div>
      </div>
    </div>


    <div class="w-full max-w-5xl">
      <div class="bg-white rounded-2xl shadow-md p-4 mt-6">
        <SiteDescription
          v-if="site"
          :descripcion_completa="site.descripcion_completa"
          :descripcion_breve="site.descripcion_breve"
        />
      </div>
    </div>


    <div class="w-full max-w-5xl">
      <div class="bg-white rounded-2xl shadow-md p-4 flex flex-col h-[260px] md:h-[320px]">
        <h2 class="text-2xl font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0L6.343 16.657a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Ubicación
        </h2>
        <div class="rounded-xl overflow-hidden border border-gray-200 flex-1">
          <SiteMap
            v-if="site && site.latitud && site.longitud"
            :latitud="site.latitud"
            :longitud="site.longitud"
            :nombre="site.nombre"
            :descripcion="site.descripcion_breve"
          />
        </div>
      </div>
    </div>

<div class="w-full max-w-5xl">
  <SiteReviews v-if="site" :site-id="site.id" />
</div>

    <!-- 🌀 Estado -->
    <div v-if="loading" class="text-gray-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import api from '@/api/axios'

import SiteHeader from '@/components/sites/SiteHeader.vue'
import SiteGallery from '@/components/sites/SiteGallery.vue'
import SiteDescription from '@/components/sites/SiteDescription.vue'
import SiteMap from '@/components/sites/SiteMap.vue'
import SiteReviews from '@/components/sites/SiteReviews.vue'

const router = useRouter()
const route = useRoute()
const site = ref(null)
const loading = ref(true)
const error = ref(null)

const { currentUser, isAuthenticated } = useAuth()


const userId = computed(() => currentUser.value?.id ?? null)

const goBack = () => router.back()

// contact card removed per user request

onMounted(async () => {
  try {
    const { id } = route.params
    const { data } = await api.get(`/sites/${id}?include_images=True`)
    site.value = data
  } catch (err) {
    console.error(err)
    error.value = 'No se pudo cargar el sitio.'
  } finally {
    loading.value = false
  }
})
</script>
