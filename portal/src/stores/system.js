// stores/system.js
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useSystemStore = defineStore('system', {
  state: () => ({
    maintenance: null,  // guarda respuesta API
    loaded: false,      // para evitar recargar varias veces
    reviewsEnabled: null,
  }),
  actions: {
    async loadStatus() {
      try {
        // Obtener mantenimiento y estado de reseñas en paralelo
        const [maintenanceRes, reviewsRes] = await Promise.all([
          axios.get('/system/maintenance'),
          axios.get('/system/reviews_enabled')
        ])

        this.maintenance = maintenanceRes.data
        this.reviewsEnabled = reviewsRes.data?.reviews_enabled ?? true
        this.loaded = true

        // Redirigir si está en mantenimiento
        if (this.maintenance?.maintenance === true && router.currentRoute.value.path !== '/maintenance') {
          router.next('/maintenance')
        }

      } catch (err) {
        console.error("Error obteniendo estado de mantenimiento:", err)
      }
    }
  }
})
