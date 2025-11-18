<template>
  <main>
    <h1>Mapa Interactivo</h1>
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      id="map"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      <l-control position="topright">
        <button v-if="showUpdateRadiusButton" @click="updateSearchRadius">
          Actualizar Radio de Búsqueda
        </button>
      </l-control>

      <l-circle :lat-lng="radiusCenter" :radius="radius" color="green" />
      <!-- <div v-for="marker in markers" :key="marker.id">
        <l-marker :lat-lng="[marker.lat, marker.lon]">
          <l-popup>
            <h3>Titulo: {{ marker.title }}</h3>
            <p>
              <span>Descripcion: {{ marker.description }}</span><br />
              <span>Creado por: {{ marker.email }}</span>
            </p>
          </l-popup>
        </l-marker>
      </div> -->
    </l-map>
  </main>
</template>

<script>
import { LControl, LCircle, LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LControl,
    LMap,
    LTileLayer,
    LCircle,
    LMarker,
    LPopup,
  },

  data() {
    return {
      zoom: 16,
      center: [-34.9225692, -57.9531812],
      radius: 0,
      radiusCenter: [ -34.9225692, -57.9531812 ],
      markers: [],
      // showUpdateRadiusButton: false,
      showErrMessage: false,
    };
  },

  computed: {
    showUpdateRadiusButton() {
      return this.centerHasChanged() || this.radius !== this.calculateNewRadius();
    }
  },

  methods: {
    zoomUpdated(newZoom) {
      this.zoom = newZoom;
    },

    centerUpdated(newCenter) {
      this.center = [newCenter.lat, newCenter.lng];
    },

    async updateSearchRadius() {
      this.radius = this.calculateNewRadius();
      this.radiusCenter = this.center;
      // await this.fetchMarkers();
    },

    // async fetchMarkers() {
    //   const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
    //   try {
    //     const response = await fetch(`${baseUrl}/api/sites/nearby`, {
    //       headers: { 'Content-Type': 'application/json' },
    //       body: JSON.stringify({
    //         latitude: this.radiusCenter[0],
    //         longitude: this.radiusCenter[1],
    //         radius: this.radius,
    //       }),
    //       method: 'POST',
    //     });
    //     const data = await response.json();
    //     this.markers = data;
    //     } catch (error) {
    //         console.error('Error fetching markers:', error);
    //         this.markers = [];
    //         this.showErrMessage = true;
    //     }
    // },

    calculateNewRadius() {
        const minRadius = 50;
        const maxRadius = 500000;
        const referenceZoom = 16;
        const referenceRadius = 500;

        const scale = Math.pow(2, referenceZoom - this.zoom);

        return Math.round(Math.max(minRadius, Math.min(maxRadius, referenceRadius * scale)));
    },

    centerHasChanged() {
        return this.radiusCenter[0] !== this.center[0] || this.radiusCenter[1] !== this.center[1];
    },

},
};
</script>
<style scoped>
  #map { height: 600px !important; width: 100% } 
  .leaflet-container { height: 100%; width: 100%; }
</style>

