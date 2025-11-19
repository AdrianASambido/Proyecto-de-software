<template>
  <div class="mt-4 w-full max-w-5xl border rounded-md bg-white shadow-sm overflow-hidden">
    <div class="px-4 py-3">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-800">Descripción</h3>
        <button @click="toggleShow" class="text-sm text-blue-600 hover:underline">
          {{ showFull ? 'Leer menos' : 'Leer más' }}
        </button>
      </div>
    </div>

    <div class="px-4 pb-4">
      <div class="text-gray-700 text-sm leading-relaxed" :style="{ maxHeight: containerMaxHeight, transition: 'max-height 300ms ease' }">
        <p v-if="!showFull" class="break-words">{{ descripcion_breve }}</p>
        <div v-else class="space-y-3">
          <p>{{ descripcion_breve }}</p>
          <p v-if="descripcion_completa">{{ descripcion_completa }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  descripcion_completa: { type: String, required: true },
  descripcion_breve:{type:String,required:true}
})

const showFull = ref(false)
const containerMaxHeight = computed(() => (showFull.value ? '1000px' : '4.5rem'))

const toggleShow = () => {
  showFull.value = !showFull.value
}
</script>
