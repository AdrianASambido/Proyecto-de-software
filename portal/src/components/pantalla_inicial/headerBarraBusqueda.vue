<template>
  <header class="header-container">
    <div class="header-content">
      <div class="logo-container" @click="goToHome" style="cursor: pointer;">
        <img src="/Image_Logo3.png" alt="Logo" class="logo-img" />
        <div class="separator-bar"></div>
        <span class="logo-text text-gray-500">Portal histórico</span>
      </div>

          <!-- Redes sociales -->
      <div class="flex items-center gap-4 mt-2">
    
        <a
          href="https://www.facebook.com/TU_PAGINA"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Facebook"
          class="text-white hover:text-teal-400
                p-1.5 border-2 rounded-full
                hover:border-teal-400 
                border-[rgb(107,106,106)]"
        >
          <!-- Facebook -->
          <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M22 12.07C22 6.48 17.52 2 11.93 2S2 6.48 2 12.07C2 17.09 5.66 21.19 10.44 21.93v-6.99H7.9v-2.87h2.54V9.41c0-2.5 1.49-3.87 3.77-3.87 1.09 0 2.23.2 2.23.2v2.45h-1.25c-1.23 0-1.61.77-1.61 1.56v1.87h2.74l-.44 2.87h-2.3V21.93C18.34 21.19 22 17.09 22 12.07z"/>
          </svg>
        </a>

        <a
          href="https://www.instagram.com/TU_PERFIL"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Instagram"
          class="text-white hover:text-teal-400
                p-1.5 border-2 rounded-full
                hover:border-teal-400
                border-[rgb(107,106,106)]"
        >
          <!-- Instagram -->
          <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2.16c3.2 0 3.584.012 4.85.07 1.17.056 1.96.24 2.42.4.6.22 1.03.48 1.48.93.45.45.71.88.93 1.48.16.46.344 1.25.4 2.42.058 1.265.07 1.65.07 4.85s-.012 3.584-.07 4.85c-.056 1.17-.24 1.96-.4 2.42-.22.6-.48 1.03-.93 1.48-.45.45-.88.71-1.48.93-.46.16-1.25.344-2.42.4-1.265.058-1.65.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.056-1.96-.24-2.42-.4-.6-.22-1.03-.48-1.48-.93-.45-.45-.71-.88-.93-1.48-.16-.46-.344-1.25-.4-2.42C2.172 15.584 2.16 15.2 2.16 12s.012-3.584.07-4.85c.056-1.17.24-1.96.4-2.42.22-.6.48-1.03.93-1.48.45-.45.88-.71 1.48-.93.46-.16 1.25-.344 2.42-.4C8.416 2.172 8.8 2.16 12 2.16zm0 1.84c-3.13 0-3.496.012-4.73.068-1.02.05-1.58.22-1.95.366-.5.19-.86.416-1.24.794-.38.38-.604.74-.794 1.24-.146.37-.316.93-.366 1.95C2.172 8.504 2.16 8.87 2.16 12s.012 3.496.068 4.73c.05 1.02.22 1.58.366 1.95.19.5.416.86.794 1.24.38.38.74.604 1.24.794.37.146.93.316 1.95.366 1.234.056 1.6.068 4.73.068s3.496-.012 4.73-.068c1.02-.05 1.58-.22 1.95-.366.5-.19.86-.416 1.24-.794.38-.38.604-.74.794-1.24.146-.37.316-.93.366-1.95.056-1.234.068-1.6.068-4.73s-.012-3.496-.068-4.73c-.05-1.02-.22-1.58-.366-1.95-.19-.5-.416-.86-.794-1.24-.38-.38-.74-.604-1.24-.794-.37-.146-.93-.316-1.95-.366C15.496 4.016 15.13 4.004 12 4.004zM12 7.2a4.8 4.8 0 110 9.6 4.8 4.8 0 010-9.6zm0 1.92a2.88 2.88 0 100 5.76 2.88 2.88 0 000-5.76zm5.1-2.58a1.12 1.12 0 11-2.24 0 1.12 1.12 0 012.24 0z"/>
          </svg>
        </a>

        <a
          href="https://x.com/TU_USUARIO"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="X"
          class="text-white hover:text-teal-400
                p-1.5 border-2 rounded-full
                hover:border-teal-400
                border-[rgb(107,106,106)]"
        >
          <!-- X (Twitter) -->
          <svg class="w- h-8" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M23 3.01c-.8.36-1.66.6-2.57.71.92-.55 1.63-1.42 1.96-2.46-.86.51-1.81.88-2.82 1.08C18.74 1.6 17.6 1 16.34 1c-1.6 0-2.9 1.3-2.9 2.9 0 .23.03.46.08.68C10.26 4.4 7.13 2.9 5 1c-.25.44-.4.95-.4 1.5 0 1.03.52 1.94 1.31 2.48-.48-.02-.93-.15-1.33-.36v.04c0 1.4.99 2.56 2.31 2.83-.24.07-.5.11-.76.11-.18 0-.36-.02-.54-.05.36 1.12 1.4 1.94 2.63 1.96-1 .78-2.26 1.25-3.63 1.25-.24 0-.47-.01-.7-.04 1.29.83 2.83 1.31 4.48 1.31 5.37 0 8.31-4.45 8.31-8.31v-.38c.57-.41 1.06-.93 1.45-1.52-.52.23-1.07.38-1.64.45.59-.36 1.05-.93 1.27-1.61z"/>
          </svg>
        </a>
      </div>
    




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
      
     
        <div v-if="isLoggedIn" class="relative">
          <button
            @click="toggleMenu"
            class="desktop-btn flex items-center gap-2 bg-gray-500 hover:bg-gray-700 px-3 py-2 rounded-lg text-sm"
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
  width: 6px;
  height: 2.5em;
  background-color: rgb(169, 17, 20); /* rgb (10, 10, 10) */
  margin: 0 15px;
}

.logo-text {
  color: rgb(107, 106, 106); /*rgb(10, 10, 10);  COLOR DEL TEXTO hover:bg-gray-700*/ 
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
