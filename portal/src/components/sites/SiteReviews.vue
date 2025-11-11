<template>
  <div class="bg-white rounded-2xl shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <svg class="w-6 h-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
        <path
          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
        />
      </svg>
      Reseñas
    </h2>

    <!-- Botón para abrir el formulario -->
    <div class="mb-4">
      <button
        @click="showForm = !showForm"
        class="px-4 py-2 bg-yellow-500 text-white font-medium rounded-lg shadow hover:bg-yellow-600 transition"
      >
        {{ showForm ? 'Cancelar' : 'Escribir reseña' }}
      </button>
    </div>

    <!-- Mostrar formulario -->
    <ReviewForm
      v-if="showForm"
      :site-id="siteId"
      @review-submitted="loadReviews"
      class="mb-6"
    />

    <!-- Lista de reseñas -->
    <div v-if="loading" class="text-gray-500">Cargando reseñas...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else-if="!reviews.length" class="text-gray-500">No hay reseñas todavía.</div>

    <ul v-else class="space-y-4">
      <li
        v-for="r in reviews"
        :key="r.id"
        class="border border-gray-100 rounded-xl p-4 bg-gray-50 hover:bg-gray-100 transition"
      >
        <div class="flex justify-between items-center mb-2">
          <span class="font-semibold text-gray-800">{{ r.usuario?.nombre || 'Usuario' }}</span>
          <span class="text-sm text-gray-400">{{ formatDate(r.fecha) }}</span>
        </div>

        <div class="flex items-center mb-1">
          <span v-for="n in 5" :key="n" class="text-yellow-400">
            <svg
              v-if="n <= r.calificacion"
              class="w-4 h-4 inline"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
              />
            </svg>
          </span>
        </div>

        <p class="text-gray-700">{{ r.contenido }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import ReviewForm from './ReviewForm.vue'

const props = defineProps({
  siteId: { type: Number, required: true },
})

const reviews = ref([])
const loading = ref(true)
const error = ref(null)
const showForm = ref(false)

const loadReviews = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/sites/${props.siteId}/reviews`)
    reviews.value = data.data
  } catch (err) {
    console.error(err)
    error.value = 'No se pudieron cargar las reseñas.'
  } finally {
    loading.value = false
  }
}

onMounted(loadReviews)

const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString()
</script>
