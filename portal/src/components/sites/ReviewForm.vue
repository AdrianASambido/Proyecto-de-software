<template>
  <form @submit.prevent="submitReview" class="border rounded-xl p-4 bg-gray-50 space-y-3">
    <label class="block">
      <span class="text-gray-700 font-medium">Calificación:</span>
      <select v-model="calificacion" class="mt-1 block w-full border rounded-lg p-2">
        <option disabled value="">Seleccioná una calificación</option>
        <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
      </select>
    </label>

    <label class="block">
      <span class="text-gray-700 font-medium">Tu reseña:</span>
      <textarea
        v-model="contenido"
        rows="3"
        class="mt-1 w-full border rounded-lg p-2 resize-none"
        placeholder="Escribí tu experiencia..."
      ></textarea>
    </label>

    <div class="flex justify-end">
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 disabled:opacity-50"
      >
        {{ loading ? 'Enviando...' : 'Publicar reseña' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const props = defineProps({
  siteId: { type: Number, required: true },
})

const emit = defineEmits(['review-submitted'])

const calificacion = ref('')
const contenido = ref('')
const loading = ref(false)

const submitReview = async () => {
  if (!calificacion.value || !contenido.value.trim()) return

  loading.value = true
  try {
    await api.post(`/sites/${props.siteId}/reviews`, {
      calificacion: calificacion.value,
      contenido: contenido.value,
    })
    emit('review-submitted') // 🔄 recargar lista
    calificacion.value = ''
    contenido.value = ''
  } catch (err) {
    console.error(err)
    alert('Error al enviar la reseña')
  } finally {
    loading.value = false
  }
}
</script>
