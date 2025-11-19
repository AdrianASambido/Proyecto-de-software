<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg relative">
      <!-- 🔙 Botón Volver -->
      <div class="absolute top-4 right-4">
        <RouterLink
          to="/"
          class="px-3 py-1.5 bg-white hover:bg-gray-100 text-gray-700 rounded-lg font-medium shadow-sm border flex items-center gap-1.5 transition text-sm"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver
        </RouterLink>
      </div>

      <div class="text-center">
        <h2 class="mt-2 text-3xl font-extrabold text-gray-900">
          Perfil de Usuario
        </h2>

      
        <img
          v-if="user?.picture"
          :src="user.picture"
          alt="Foto de perfil"
          class="mx-auto mt-4 w-32 h-32 rounded-full object-cover shadow-md"
        />

      
        <div
          v-else
          class="mx-auto mt-4 w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-4xl"
        >
          ?
        </div>
      </div>

      <div v-if="user" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="p-4 border rounded-t-md">
            <p class="font-medium text-gray-700">Nombre</p>
            <p class="text-gray-900">{{ user.nombre }}</p>
          </div>
          <div class="p-4 border rounded-b-md">
            <p class="font-medium text-gray-700">Email</p>
            <p class="text-gray-900">{{ user.email }}</p>
          </div>
        </div>
      </div>

      <div v-else>
        <p>Cargando...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const user = ref(null)

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
  }
})
</script>
