<template>
  <div class="maintenance flex flex-col items-center justify-center min-h-screen p-4">
    <h1 class="text-3xl font-bold">Mantenimiento en progreso</h1>
    <p class="mt-4">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('')

onMounted(async () => {
  const { data } = await axios.get('/system/maintenance')
  message.value = data.message
})
</script>
