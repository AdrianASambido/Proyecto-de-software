<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-[9999] flex items-center justify-center bg-black bg-opacity-50"
  >
    <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-sm w-full relative animate-fade-in">
      <!-- Botón cerrar -->
      <button
        @click="emit('update:modelValue', false)"
        class="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
      >
        ✕
      </button>
 
      <h2 class="text-2xl font-semibold text-gray-900 mb-3 text-center">
        Inicia sesión para continuar
      </h2>

     
      <p class="text-gray-600 text-center mb-6 px-2">
        Para realizar esta acción, necesitamos que inicies sesión con tu cuenta de Google.
      </p>

     
      <div class="flex justify-center">
        <GoogleLoginButton @logged-in="onLoginSuccess" />
      </div>

     
    </div>
  </div>
</template>

<script setup>
import GoogleLoginButton from './login.vue'

defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'logged-in'])

function onLoginSuccess(user) {
  emit('logged-in', user)
  emit('update:modelValue', false)
   window.location.reload();
}
</script>

<style scoped>
:host {
  position: relative;
  z-index: 9999;
}

@keyframes fade-in {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>
