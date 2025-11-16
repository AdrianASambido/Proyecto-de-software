// stores/system.js
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

export const useSystemStore = defineStore('system', {
  state: () => ({
    maintenance: null,  // guarda respuesta API
    loaded: false,      // para evitar recargar varias veces
  }),

  actions: {
    async loadStatus() {
      if (this.loaded) return   // evita llamadas duplicadas

      try {
        const { data } = await axios.get('/system/maintenance')
        this.maintenance = data
        this.loaded = true

        // Redirigir si está en mantenimiento
        if (data?.maintenance === true) {
          router.push('/maintenance')
        }

      } catch (err) {
        console.error("Error obteniendo estado de mantenimiento:", err)
      }
    }
  }
})
