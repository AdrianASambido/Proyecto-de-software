<template>
  <GaleriaTarjetasMonumentos
    :items="items"
    :loading="loading"
    :error="error"
    title="Recientemente Agregados"
    :view-all-route="viewAllRoute"
    empty-message="No hay sitios recientes disponibles"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GaleriaTarjetasMonumentos from './galeriaTarjetasMonumentos.vue'
import { useSites } from '@/composables/useSites'

const router = useRouter()
const { loading, error, fetchRecientementeAgregados } = useSites()
const items = ref([])

// Ruta para "Ver todos" con el filtro de orden aplicado
const viewAllRoute = {
  path: '/sitios',
  query: { order: 'fecha_desc' }
}

// Carga perezosa
const loadData = async () => {
  if (loading.value || items.value.length > 0) return
  
  const data = await fetchRecientementeAgregados()
  items.value = data
}

onMounted(() => {
  loadData()
})
</script>

