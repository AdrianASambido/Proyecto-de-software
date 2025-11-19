<template>
  <div class="w-full h-full">
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      class="w-full h-full"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      <l-control position="topright">
        <button 
          v-if="showUpdateRadiusButton" 
          @click="updateSearchRadius"
          class="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded text-sm font-medium shadow-lg"
        >
          Actualizar Radio de Búsqueda
        </button>
      </l-control>

      <l-circle :lat-lng="radiusCenter" :radius="radius" color="green" />
    </l-map>
  </div>
</template>

<script>
import { LControl, LCircle, LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LControl,
    LMap,
    LTileLayer,
    LCircle,
  },

  emits: ['update-location'],

  data() {
    return {
      zoom: 6,
      center: [-34.6037, -58.3816],
      radius: 0,
      radiusCenter: [-34.6037, -58.3816],
    };
  },

  mounted() {
    // Calcular radio inicial
    this.radius = this.calculateNewRadius();
    this.radiusCenter = this.center;
    this.emitLocation();
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

    updateSearchRadius() {
      this.radius = this.calculateNewRadius();
      this.radiusCenter = this.center;
      this.emitLocation();
    },

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

    emitLocation() {
      const radiusKm = Math.round(this.radius / 1000);
      this.$emit('update-location', {
        latitud: this.radiusCenter[0],
        longitud: this.radiusCenter[1],
        radio: Math.max(radiusKm, 1)
      });
    },
  },

  watch: {
    zoom() {
      // Cuando cambia el zoom, actualizar el radio calculado pero no emitir hasta que se presione el botón
    },
    center() {
      // Cuando cambia el centro, verificar si debe mostrarse el botón
    }
  }
};
</script>
<style scoped>
  .leaflet-container { height: 100%; width: 100%; }
</style>

