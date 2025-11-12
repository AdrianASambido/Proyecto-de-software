<template>
  <!-- Fondo semi-transparente -->
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
    @click.self="close"
  >
    <!-- Contenedor del popup -->
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 relative text-center animate-fade-in">
      <!-- Botón de cierre -->
      <button
        @click="close"
        class="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
      >
        ✕
      </button>

      <h2 class="text-xl font-semibold text-gray-800 mb-4">
        Inicia sesión para continuar
      </h2>

      <p class="text-gray-500 text-sm mb-6">
        Usa tu cuenta de Google para acceder rápidamente
      </p>

      <!-- Aquí va tu botón Google reutilizado -->
      <GoogleLoginButton @logged-in="onLoginSuccess" />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"
import GoogleLoginButton from "@/components/login_google/login.vue"

const props = defineProps({
  modelValue: { type: Boolean, required: true },
})

const emit = defineEmits(["update:modelValue", "login"])

function close() {
  emit("update:modelValue", false)
}

function onLoginSuccess(user) {
  emit("login", user)
  close()
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>
