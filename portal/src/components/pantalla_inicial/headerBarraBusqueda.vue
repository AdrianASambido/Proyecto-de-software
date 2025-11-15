<template>
  <header class="header-container">
    <div class="header-content">
      <div class="logo-container" @click="goToHome" style="cursor: pointer;">
        <img src="/Image_Logo3.png" alt="Logo" class="logo-img" />
        <div class="separator-bar"></div>
        <span class="logo-text">Portal histórico</span>
      </div>

<!--- <div class="buscador-rapido">
        <button class="btn-busqueda" @click="goToSites">Buscar</button>
      </div> 
  <header class="w-full bg-gray-900 text-white shadow-md relative">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between"> -->

      <!-- MOBILE MENU BUTTON -->
      <button
        class="md:hidden text-3xl"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        ☰
      </button>

      <!-- DESKTOP MENU -->
      <div class="hidden md:flex items-center gap-6">

        <button
          @click="goToSites"
          class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md text-sm"
        >
          Buscar
        </button>

     
        <div v-if="isLoggedIn" class="relative">
          <button
            @click="toggleMenu"
            class="desktop-btn flex items-center gap-2 bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-lg text-sm"
          >
            <img
              v-if="user?.picture"
              :src="user.picture"
              class="w-8 h-8 rounded-full object-cover"
            />

            <span>{{ user?.nombre || user?.email }}</span>

            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <transition name="fade">
            <div
              v-if="menuOpen"
              class="dropdown-menu absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-lg shadow-lg overflow-hidden z-50"
            >
              <router-link to="/perfil" class="menu-item" @click="toggleMenu">Perfil</router-link>
              <router-link to="/mis-resenas" class="menu-item" @click="toggleMenu">Mis reseñas</router-link>
              <router-link to="/favoritos" class="menu-item" @click="toggleMenu">Sitios favoritos</router-link>
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


    <div
      v-show="mobileMenuOpen"
      class="md:hidden absolute top-full left-0 w-full bg-gray-800 px-4 pt-4 pb-6 space-y-4 shadow-lg z-50"
    >
      <button
        @click="goToSites"
        class="w-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md text-sm"
      >
        Buscar
      </button>

   <div v-if="isLoggedIn" class="space-y-4">

    
        <div class="flex items-center gap-3 px-2">
          <img
            v-if="user?.picture"
            :src="user.picture"
            class="w-10 h-10 rounded-full object-cover"
          />
          <span class="text-white text-lg font-medium">
            {{ user?.nombre || username }}
          </span>
        </div>

        <router-link to="/perfil" class="mobile-item">Perfil</router-link>
        <router-link to="/mis-resenas" class="mobile-item">Mis reseñas</router-link>
        <router-link to="/favoritos" class="mobile-item">Sitios favoritos</router-link>

        <button @click="handleLogout" class="w-full text-left mobile-item text-red-400">
          Cerrar sesión
        </button>
      </div>


      <div v-else>
        <GoogleLoginButton @logged-in="handleLoginSuccess" />
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import GoogleLoginButton from '@/components/login_google/login.vue'

const isLoggedIn = ref(false)
const user = ref(null)       
const menuOpen = ref(false)
const mobileMenuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = (e) => {
  const dropdown = e.target.closest('.desktop-menu')
  const dropdownBtn = e.target.closest('.desktop-btn')

  if (!dropdown && !dropdownBtn) {
    menuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeMenu)

  const savedUser = localStorage.getItem('user')
  const savedToken = localStorage.getItem('token')

  if (savedUser && savedToken) {
    user.value = JSON.parse(savedUser)   
    isLoggedIn.value = true
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeMenu)
})

const handleLoginSuccess = (u) => {
  user.value = u                 
  isLoggedIn.value = true
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  isLoggedIn.value = false
  window.location.reload()
}

const goToSites = () => {
  window.location.href = '/sitios'
}

const goToHome = () => {
  window.location.href = '/'
}
</script>

<style scoped>

.header-container {
  background-color: #ece8e8; /* #333 es un gris oscuro*/
  padding: 15px 0px 15px 20px;
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
  align-items: stretch;
  max-width: 100%;
  width: 100%;
  gap: 0;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0px;
}

.logo-img {
  height: 70px; /* Ajusta el tamaño según sea necesario */
  width: auto;
}

.separator-bar {
  width: 2px;
  height: 2.5em;
  background-color: rgb(10, 10, 10);
  margin: 0 15px;
}

.logo-text {
  color: rgb(10, 10, 10);
  font-size: 1.8rem;
  font-weight: bold;
}

/*/.buscador-rapido {
  display: flex;
  gap: 5px;
}*/

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

.auth-section {
display: flex;
align-items: stretch;
justify-content: center;
height: 80%;
padding: 0 20px;
margin-right: 56px; /* desplaza el botón ~1.5cm hacia el centro */
}

.menu-item {
  @apply block px-4 py-2 hover:bg-gray-100 text-sm;
}
.mobile-item {
  @apply block w-full px-4 py-2 bg-gray-700 text-white rounded-md;
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
