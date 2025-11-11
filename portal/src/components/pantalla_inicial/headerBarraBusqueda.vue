<template>
  <header class="header-container">
    <div class="header-content">
      <div class="logo-container">
        <img src="/Image_Logo3.png" alt="Logo" class="logo-img" />
      </div>


      <div class="buscador-rapido">
        <button class="btn-busqueda" @click="goToSites">Buscar</button>
      </div>

    
      <div class="auth-section">

        <div v-if="isLoggedIn" class="relative">
          <button
            @click="toggleMenu"
            class="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-lg text-sm font-medium transition"
          >
            <span>👤 {{ username }}</span>
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <transition name="fade">
            <div
              v-if="menuOpen"
              class="absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-lg shadow-lg overflow-hidden z-50"
            >
              <a href="/perfil" class="menu-item">Perfil</a>
              <a href="/mis-resenas" class="menu-item">Mis reseñas</a>
              <a href="/favoritos" class="menu-item">Sitios favoritos</a>
              <button @click="handleLogout" class="menu-item text-red-600 hover:bg-red-50">
                Cerrar sesión
              </button>
            </div>
          </transition>
        </div>


        <div v-else>
          <GoogleLoginButton @logged-in="handleLoginSuccess" />
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import GoogleLoginButton from '@/components/login_google/login.vue'

const isLoggedIn = ref(false)
const username = ref('')
const searchTerm = ref('')
const menuOpen = ref(false)

const emit = defineEmits(['search'])

const performSearch = () => {
  emit('search', searchTerm.value)
}

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = (e) => {
  if (!e.target.closest('.relative')) menuOpen.value = false
}


onMounted(() => {
  document.addEventListener('click', closeMenu)
  const savedUser = localStorage.getItem('user')
  const savedToken = localStorage.getItem('token')
  if (savedUser && savedToken) {
    const user = JSON.parse(savedUser)
    username.value = user.nombre || user.email
    isLoggedIn.value = true
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeMenu)
})

const handleLoginSuccess = (user) => {
  username.value = user.nombre || user.email
  isLoggedIn.value = true
  console.log('Usuario logueado:', user)
}

const handleLogout = () => {
  isLoggedIn.value = false
  username.value = ''
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  window.location.reload()
}
</script>

<style scoped>

.header-container {
  background-color: #333;
  padding: 15px 20px;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  width: 100%;
  box-sizing: border-box;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  width: 100%;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-img {
  height: 200px; /* Ajusta el tamaño según sea necesario */
  width: auto;
}

.buscador-rapido {
  display: flex;
  gap: 5px;
}

.input-busqueda {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  width: 200px;
}

.btn-busqueda {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-busqueda:hover {
  background-color: #0056b3;
}


.menu-item {
  display: block;
  padding: 10px 15px;
  font-size: 0.95em;
  transition: background-color 0.2s ease;
}
.menu-item:hover {
  background-color: #f5f5f5;
}


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
