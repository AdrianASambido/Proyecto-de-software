<template>
  <GaleriaTarjetasMonumentos
    :items="items"
    :loading="loading"
    :error="error"
    title="Mejor Puntuados"
    :view-all-route="viewAllRoute"
    empty-message="No hay sitios con calificaciones disponibles"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GaleriaTarjetasMonumentos from './galeriaTarjetasMonumentos.vue'
import { useSites } from '@/composables/useSites'

const router = useRouter()
const { loading, error, fetchMejorPuntuados } = useSites()
const items = ref([])

// Ruta para "Ver todos" con el filtro de orden aplicado
const viewAllRoute = {
  path: '/sitios',
  query: { order: 'mejor_puntuado' }
}
// Carga perezosa: solo se carga cuando el componente es visible
let observer = null

const loadData = async () => {
  if (loading.value || items.value.length > 0) return
  
  const data = await fetchMejorPuntuados()
  items.value = data
}
// Usar Intersection Observer para carga perezosa
onMounted(() => {
  // Cargar inmediatamente (puedes cambiar esto para usar Intersection Observer si prefieres)
  loadData()
})
</script>

<style scoped>
.seccion-mejor-puntuados {
  min-height: 200px;
}
</style>

