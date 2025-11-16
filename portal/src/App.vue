<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toaster } from 'vue-sonner'

import HeaderBarraBusqueda from './components/pantalla_inicial/headerBarraBusqueda.vue'
import HeroPrincipal from './components/pantalla_inicial/heroPrincipal.vue'
import Footer from './components/pantalla_inicial/Footer.vue'

import { useSystemStore } from './stores/system'

// Store
const system = useSystemStore()

// Router
const router = useRouter()

// Cargar estado del sistema una sola vez
onMounted(async () => {
  await system.loadStatus()
})

// Buscador
const handleSearch = (searchTerm) => {
  router.push({ path: '/', query: { search: searchTerm } })
}
</script>

<template>
  <Toaster position="bottom-right" richColors />
  <HeaderBarraBusqueda @search="handleSearch" />

  <main>
    <router-view />
  </main>

  <Footer />
</template>

<style scoped></style>
