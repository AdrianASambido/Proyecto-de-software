<template>
  <div id="map" class="w-full h-full rounded-xl"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  latitud: Number,
  longitud: Number,
  nombre: String,
  descripcion: String
})

onMounted(() => {
  const map = L.map('map', {
    scrollWheelZoom: false,
    zoomControl: true
  }).setView([props.latitud, props.longitud], 14)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  L.marker([props.latitud, props.longitud])
    .addTo(map)
    .bindPopup(`<b>${props.nombre}</b><br>${props.descripcion}`)
})
</script>
