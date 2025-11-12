<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Perfil de Usuario
        </h2>
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
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
import { ref, onMounted } from 'vue';

const user = ref(null);

onMounted(() => {
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    user.value = JSON.parse(savedUser);
  }
});
</script>

<style scoped>
h1 {
  color: #333;
}
</style>
