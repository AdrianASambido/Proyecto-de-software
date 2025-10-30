<template>
  <div class="mt-4 w-full max-w-5xl border rounded-md bg-white shadow-sm">
    <!-- Botón desplegable -->
    <button
      @click="toggleShow"
      class="w-full flex justify-between items-center px-4 py-2 text-left text-gray-700 font-medium hover:bg-gray-100 rounded-md focus:outline-none"
    >
      <span>{{ showFull ? 'Ver menos' : 'Ver más' }}</span>
      <svg
        :class="{'rotate-180': showFull, 'rotate-0': !showFull}"
        class="w-5 h-5 transition-transform duration-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>

    <!-- Contenedor del contenido -->
    <div
      ref="content"
      class="overflow-hidden px-4 transition-[max-height] duration-300 ease-in-out"
      :style="{ maxHeight: maxHeight }"
    >
      <p
        class="py-3 text-gray-600 transition-opacity duration-300"
        :style="{ opacity: showFull ? 1 : 0 }"
      >
        {{  descripcion_breve }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  descripcion_breve: { type: String, required: true }
})

const showFull = ref(false)
const content = ref(null)
const maxHeight = ref('0px')

const toggleShow = async () => {
  showFull.value = !showFull.value
  await nextTick()
  if (showFull.value && content.value) {
    // altura real del contenido
    maxHeight.value = content.value.scrollHeight + 'px'
  } else {
    maxHeight.value = '0px'
  }
}
</script>
