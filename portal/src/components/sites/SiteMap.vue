<template>
  <div
    ref="mapContainer"
    class="w-full h-[420px] rounded-xl overflow-hidden shadow-inner border border-gray-200"
  ></div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  latitud: { type: Number, required: true },
  longitud: { type: Number, required: true },
  nombre: { type: String, required: true },
  descripcion: { type: String, default: '' }
})

const mapContainer = ref(null)

onMounted(async () => {
  await nextTick()
  const map = L.map(mapContainer.value).setView([props.latitud, props.longitud], 14)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
  }).addTo(map)

  const marker = L.marker([props.latitud, props.longitud]).addTo(map)
  marker.bindPopup(`<b>${props.nombre}</b><br>${props.descripcion}`).openPopup()
})
</script>
