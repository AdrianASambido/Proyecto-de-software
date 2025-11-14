<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg">
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

        <router-link
          to="/"
          class="group w-full flex justify-center py-2 px-4 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
        >
          Volver a la página principal
        </router-link>
      </div>

      <div v-else>
        <p>Cargando...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const user = ref(null)

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
  }
})
</script>
