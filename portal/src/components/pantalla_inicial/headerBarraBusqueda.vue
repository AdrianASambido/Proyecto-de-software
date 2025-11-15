<template>
  <header class="header-container relative">
    <div class="header-content">

      <!-- LOGO -->
      <div class="logo-container" @click="goToHome" style="cursor: pointer;">
        <img src="/Image_Logo3.png" alt="Logo" class="logo-img" />
        <div class="separator-bar"></div>
        <span class="logo-text">Portal histórico</span>
      </div>


      <button
        class="md:hidden text-3xl text-black pr-4"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        ☰
      </button>


      <div class="hidden md:flex items-center gap-6">

        <button
          @click="goToSites" 
          class="
            bg-transparent                      
            text-red-700                      
            border border-red-700            
            hover:bg-portal-red                   
            hover:text-portal-red          
            px-4 py-2 rounded-md text-sm

            /* CAMBIO AL PASAR EL RATÓN (HOVER) */
            hover:bg-transparent                        /* Se vuelve transparente al pasar el ratón */
            hover:text-gray-900                         /* El texto se vuelve gris oscuro */
            hover:border-gray-900                       /* El borde se vuelve gris oscuro */

            transition-colors duration-200   "
        >
          Buscar
        </button>
    


        <div v-if="isLoggedIn" class="relative desktop-menu">
          <button
            @click="toggleMenu"
            class="desktop-btn flex items-center gap-2 bg-gray-900 hover:bg-gray-800 text-white px-3 py-2 rounded-lg text-sm"
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
              class="dropdown-menu absolute right-0 mt-2 w-48 bg-white text-black rounded-lg shadow-lg overflow-hidden z-50"
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

  
    <transition name="fade">
      <div
        v-if="mobileMenuOpen"
        class="md:hidden absolute right-4 top-full mt-2 w-56 bg-white text-black rounded-lg shadow-lg p-4 z-50"
      >
        <button
          @click="navAndClose('/sitios')"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm mb-2"
        >
          Buscar
        </button>

        <div v-if="isLoggedIn" class="space-y-2">
          <router-link to="/perfil" @click="closeMobileMenu" class="mobile-item">Perfil</router-link>
          <router-link to="/mis-resenas" @click="closeMobileMenu" class="mobile-item">Mis reseñas</router-link>
          <router-link to="/favoritos" @click="closeMobileMenu" class="mobile-item">Sitios favoritos</router-link>

          <button @click="handleLogout" class="mobile-item text-red-500">Cerrar sesión</button>
        </div>

        <div v-else>
          <GoogleLoginButton @logged-in="handleLoginSuccess" />
        </div>
      </div>
    </transition>

  </header>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue"
import { useRouter } from "vue-router"
import GoogleLoginButton from "@/components/login_google/login.vue"

const router = useRouter()

const isLoggedIn = ref(false)
const user = ref(null)
const menuOpen = ref(false)
const mobileMenuOpen = ref(false)

const toggleMenu = () => (menuOpen.value = !menuOpen.value)
const closeMobileMenu = () => (mobileMenuOpen.value = false)

onMounted(() => {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".desktop-btn")
    const menu = e.target.closest(".desktop-menu")
    if (!btn && !menu) menuOpen.value = false
  })

  const savedUser = localStorage.getItem("user")
  const savedToken = localStorage.getItem("token")

  if (savedUser && savedToken) {
    user.value = JSON.parse(savedUser)
    isLoggedIn.value = true
  }
})

const handleLoginSuccess = (u) => {
  user.value = u
  isLoggedIn.value = true
}

const handleLogout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("user")
  user.value = null
  isLoggedIn.value = false
  location.reload()
}

const navAndClose = (path) => {
  mobileMenuOpen.value = false
  router.push(path)
}

const goToSites = () => router.push("/sitios")
const goToHome = () => router.push("/")
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
  width: 6px;
  height: 2.5em;
  background-color: rgb(169, 17, 20); /* rgb (10, 10, 10) */
  margin: 0 15px;
}

.logo-text {
  color: rgb(10, 10, 10); /* COLOR DEL TEXTO hover:bg-gray-700*/ 
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
  background-color: rgb(169, 17, 20); /* #007bff;*/
  color: white;
  border: rgb(169, 17, 20); /* NONE */
  padding: 8px 12px;
  border-radius: 15px;
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
  display: block;
  padding: 10px 16px;
}

.mobile-item {
  display: block;
  padding: 8px;
  border-radius: 6px;
  background: #f3f3f3;
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
