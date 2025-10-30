<template>
  <header class="space-y-3">
    <!-- Encabezado principal: título y rating -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
      <h1 class="text-3xl font-bold text-gray-900">
        {{ site.nombre }}
      </h1>

      <div class="flex items-center space-x-2">
        <div class="flex items-center space-x-1">
          <template v-for="n in 5" :key="n">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              class="w-5 h-5"
              :class="n <= Math.round(site.valoracion) ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor"
            >
              <path
                d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.782 1.401 8.171L12 18.896l-7.335 3.867 1.401-8.171L.132 9.21l8.2-1.192z"
              />
            </svg>
          </template>
        </div>
        <span class="text-sm text-gray-600">
          {{ site.valoracion?.toFixed(1) || '0.0' }} ({{ site.cantidad_resenas || 0 }} reseñas)
        </span>
      </div>
    </div>

    <!-- Línea divisoria -->
    <hr class="border-gray-200" />

    <!-- Detalles secundarios -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-sm text-gray-700">
      <div>
        <span class="font-semibold text-gray-900">Ubicación:</span>
        <span>{{ site.ciudad }}, {{ site.provincia }}</span>
      </div>

      <div>
        <span class="font-semibold text-gray-900">Estado de conservación:</span>
        <span
          class="ml-2 inline-block px-3 py-1 rounded-full text-xs font-semibold"
          :class="statusColor(site.estado_conservacion)"
        >
          {{ site.estado_conservacion }}
        </span>
      </div>
    </div>
  </header>
</template>


<script setup>
const props = defineProps({
  site: {
    type: Object,
    required: true,
    default: () => ({
      nombre: '',
      ciudad: '',
      provincia: '',
      estado_conservacion: 'Bueno',
      valoracion: 0,
      cantidad_resenas: 0
    })
  }
})



const statusColor = (status) => {
  switch (status) {
    case 'Bueno':
      return 'bg-blue-100 text-blue-800'
    case 'Regular':
      return 'bg-yellow-100 text-yellow-800'
    case 'Malo':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-700'
  }
}
</script>

<style scoped>
svg {
  transition: color 0.2s ease;
}
</style>
