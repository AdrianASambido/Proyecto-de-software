<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="$emit('cancel')"></div>
        <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6">
            <h3 class="text-xl font-semibold mb-4">Editar Reseña</h3>

            <form @submit.prevent="handleSubmit">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Calificación
                </label>
                <select
                  v-model="rating"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option disabled value="">Seleccioná una calificación</option>
                  <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
                </select>
              </div>

              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Contenido
                </label>
                <textarea
                  v-model="content"
                  rows="6"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  :class="{ 'border-red-500': content.length > 0 && content.length < 20 }"
                  placeholder="Escribe tu reseña aquí (mínimo 20 caracteres)..."
                ></textarea>
                <div class="flex justify-between items-center mt-1">
                  <span
                    v-if="content.length > 0 && content.length < 20"
                    class="text-sm text-red-600"
                  >
                    Mínimo 20 caracteres
                  </span>
                  <span class="text-sm ml-auto" :class="characterCountColor">
                    {{ content.length }}/1000
                  </span>
                </div>
              </div>

              <div class="flex justify-end gap-3">
                <button
                  type="button"
                  @click="$emit('cancel')"
                  class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="!isValid || loading"
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ loading ? 'Guardando...' : 'Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  review: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const rating = ref('')
const content = ref('')

watch(() => props.show, (newVal) => {
  if (newVal && props.review) {
    rating.value = props.review.calificacion
    content.value = props.review.contenido
  }
})

const isValid = computed(() => {
  return rating.value > 0 && content.value.length >= 20 && content.value.length <= 1000
})

const characterCountColor = computed(() => {
  const length = content.value.length
  if (length < 20) return 'text-gray-500'
  if (length > 1000) return 'text-red-600'
  if (length > 900) return 'text-yellow-600'
  return 'text-green-600'
})

const handleSubmit = () => {
  if (isValid.value) {
    emit('confirm', {
      calificacion: rating.value,
      contenido: content.value
    })
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.9);
}
</style>
