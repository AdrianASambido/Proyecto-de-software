<template>
  <div>
    <div v-if="existingReview" class="border rounded-xl p-4 bg-blue-50 space-y-3">
      <p class="text-blue-800 font-medium">Ya has dejado una reseña para este sitio</p>
      <p class="text-blue-600 text-sm">Estado: {{ getEstadoLabel(existingReview.estado) }}</p>
    </div>

    <form v-else @submit.prevent="submitReview" class="border rounded-xl p-4 bg-gray-50 space-y-3">
      <label class="block">
        <span class="text-gray-700 font-medium">Calificación:</span>
        <select
          v-model="calificacion"
          class="mt-1 block w-full border rounded-lg p-2"
          :class="{ 'border-red-500': errors.calificacion }"
        >
          <option disabled value="">Seleccioná una calificación</option>
          <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
        </select>
        <p v-if="errors.calificacion" class="text-red-500 text-sm mt-1">{{ errors.calificacion }}</p>
      </label>

      <label class="block">
        <span class="text-gray-700 font-medium">Tu reseña:</span>
        <textarea
          v-model="contenido"
          rows="4"
          class="mt-1 w-full border rounded-lg p-2 resize-none"
          :class="{ 'border-red-500': errors.contenido }"
          placeholder="Escribí tu experiencia... (mínimo 20 caracteres)"
          maxlength="1000"
        ></textarea>
        <div class="flex justify-between items-center mt-1">
          <p v-if="errors.contenido" class="text-red-500 text-sm">{{ errors.contenido }}</p>
          <p
            class="text-sm ml-auto"
            :class="contenido.length < 20 ? 'text-gray-400' : 'text-gray-600'"
          >
            {{ contenido.length }}/1000
          </p>
        </div>
      </label>

      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
        <p class="text-yellow-800 text-sm">
          Tu reseña será revisada antes de publicarse.
        </p>
      </div>

      <div class="flex justify-end">
        <button
          type="submit"
          :disabled="loading"
          class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 disabled:opacity-50 transition-colors"
        >
          {{ loading ? 'Enviando...' : 'Publicar reseña' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useReviews } from '@/composables/useReviews'
import { useAuth } from '@/composables/useAuth'

const props = defineProps({
  siteId: { type: Number, required: true },
})

const emit = defineEmits(['review-submitted'])

const { createReview, checkUserHasReview } = useReviews()
const { isAuthenticated } = useAuth()

const calificacion = ref('')
const contenido = ref('')
const loading = ref(false)
const errors = ref({})
const existingReview = ref(null)

const validate = () => {
  errors.value = {}

  if (!calificacion.value) {
    errors.value.calificacion = 'Selecciona una calificación'
  }

  if (!contenido.value.trim()) {
    errors.value.contenido = 'El contenido es requerido'
  } else if (contenido.value.trim().length < 20) {
    errors.value.contenido = 'Mínimo 20 caracteres'
  } else if (contenido.value.length > 1000) {
    errors.value.contenido = 'Máximo 1000 caracteres'
  }

  return Object.keys(errors.value).length === 0
}

const submitReview = async () => {
  if (!validate()) return

  loading.value = true
  try {
    await createReview(props.siteId, {
      calificacion: calificacion.value,
      contenido: contenido.value.trim(),
    })

    calificacion.value = ''
    contenido.value = ''
    errors.value = {}

    emit('review-submitted')

    await checkExistingReview()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const checkExistingReview = async () => {
  if (!isAuthenticated.value) return
  existingReview.value = await checkUserHasReview(props.siteId)
}

const getEstadoLabel = (estado) => {
  const labels = {
    'pendiente': 'Pendiente de aprobación',
    'aprobada': 'Aprobada',
    'rechazada': 'Rechazada'
  }
  return labels[estado] || estado
}

onMounted(() => {
  checkExistingReview()
})
</script>
