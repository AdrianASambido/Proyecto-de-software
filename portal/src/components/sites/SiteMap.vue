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
const customIcon = L.divIcon({
  html: `
    <div class="w-6 h-6 bg-blue-600 rounded-full border-2 border-white shadow-lg"></div>
  `,
  className: '', 
  iconSize: [24, 24],
  iconAnchor: [12, 12]
})


onMounted(() => {
  const map = L.map('map', {
    scrollWheelZoom: false,
    zoomControl: true
  }).setView([props.latitud, props.longitud], 14)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

const marker = L.marker([props.latitud, props.longitud], { icon: customIcon })
  .addTo(map)
  .bindPopup(`<b>${props.nombre}</b><br>${props.descripcion}`)
  .openPopup()

})
</script>
