
<template>
  <header class="header-container relative">
    <div class="header-content">

      <!-- LOGO -->
      <div class="logo-and-social">
        <div class="logo-container" @click="goToHome" style="cursor: pointer;">
          <img src="/Image_Logo3.png" alt="Logo" class="logo-img" />
          <div class="separator-bar"></div>
          <span class="logo-text text-gray-500">Portal histórico</span>
        </div>

        <!-- Redes siempre visibles en desktop y mobile gap-3 mt-2 md:mt-0 md:ml-4 -->
        <div class="socials flex items-center justify-center flex-grow gap-4 mt-2 md:mt-0 md:ml-4">
          <a href="https://www.facebook.com/InfoUNLP" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="social-btn text-gray-500">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M22 12.07C22 6.48 17.52 2 11.93 2S2 6.48 2 12.07C2 17.09 5.66 21.19 10.44 21.93v-6.99H7.9v-2.87h2.54V9.41c0-2.5 1.49-3.87 3.77-3.87 1.09 0 2.23.2 2.23.2v2.45h-1.25c-1.23 0-1.61.77-1.61 1.56v1.87h2.74l-.44 2.87h-2.3V21.93C18.34 21.19 22 17.09 22 12.07z"/></svg>
          </a>
          <a href="https://www.instagram.com/informaticaunlp" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="social-btn text-gray-500">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M12 2.163c3.204 0 3.584.012 4.85.07 1.266.057 2.122.242 2.88.547.748.305 1.45 1.45 2.138 2.138.305.748.547 1.614.547 2.88.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.057 1.266-.242 2.122-.547 2.88-.305.748-1.45 1.45-2.138 2.138-.748.305-1.614.547-2.88.547-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.266-.057-2.122-.242-2.88-.547-.748-.305-1.45-1.45-2.138-2.138-.305-.748-.547-1.614-.547-2.88-.058-1.266-.07-1.646-.07-4.85s.012-3.584.07-4.85c.057-1.266.242-2.122.547-2.88.305-.748 1.45-1.45 2.138-2.138.748-.305 1.614-.547 2.88-.547 1.266-.058 1.646-.07 4.85-.07zM12 4.865c-3.126 0-3.492.012-4.71.068-1.02.048-1.58.22-1.95.367-.5.19-.86.417-1.24.795-.38.38-.604.74-.795 1.24-.147.37-.318.93-.367 1.95-.056 1.218-.068 1.584-.068 4.71s.012 3.492.068 4.71c.048 1.02.22 1.58.367 1.95.19.5.417.86.795 1.24.38.38.74.604 1.24.795.37.147.93.318 1.95.367 1.218.056 1.584.068 4.71.068s3.492-.012 4.71-.068c1.02-.048 1.58-.22 1.95-.367.5-.19.86-.417 1.24-.795.38-.38.604-.74.795-1.24.147-.37.318-.93.367-1.95.056-1.218.068-1.584.068-4.71s-.012-3.492-.068-4.71c-.048-1.02-.22-1.58-.367-1.95-.19-.5-.417-.86-.795-1.24-.38-.38-.74-.604-1.24-.795-.37-.147-.93-.318-1.95-.367-1.218-.056-1.584-.068-4.71-.068zM12 9.163a2.837 2.837 0 100 5.674 2.837 2.837 0 000-5.674zm0 7.5a4.663 4.663 0 110-9.326 4.663 4.663 0 010 9.326zM16.837 8.163a1.163 1.163 0 11-2.326 0 1.163 1.163 0 012.326 0z" clip-rule="evenodd"/>
            </svg>
          </a>
          <a href="https://x.com/InformaticaUNLP" target="_blank" rel="noopener noreferrer" aria-label="X" class="social-btn text-gray-500">
            <svg preserveAspectRatio="xMidYMid meet" class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3.01c-.8.36-1.66.6-2.57.71.92-.55 1.63-1.42 1.96-2.46-.86.51-1.81.88-2.82 1.08C18.74 1.6 17.6 1 16.34 1c-1.6 0-2.9 1.3-2.9 2.9 0 .23.03.46.08.68C10.26 4.4 7.13 2.9 5 1c-.25.44-.4.95-.4 1.5 0 1.03.52 1.94 1.31 2.48-.48-.02-.93-.15-1.33-.36v.04c0 1.4.99 2.56 2.31 2.83-.24.07-.5.11-.76.11-.18 0-.36-.02-.54-.05.36 1.12 1.4 1.94 2.63 1.96-1 .78-2.26 1.25-3.63 1.25-.24 0-.47-.01-.7-.04 1.29.83 2.83 1.31 4.48 1.31 5.37 0 8.31-4.45 8.31-8.31v-.38c.57-.41 1.06-.93 1.45-1.52-.52.23-1.07.38-1.64.45.59-.36 1.05-.93 1.27-1.61z"/></svg>
          </a>
        </div>
      </div>
    
      <!-- Hamburguesa oculta en mantenimiento -->



      <!-- MOBILE MENU BUTTON -->
      <button v-if="!isMaintenance" class="hamburger md:hidden" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Abrir menú">
        ☰
      </button>


      <!-- MENU DESKTOP -->
      <div v-if="!isMaintenance" class="menu-desktop hidden md:flex items-center gap-6">
        <button
    @click="goToSites" 
    class="
        /* ESTADO NORMAL: Fondo rojo (red-700) y texto blanco */
        bg-red-700
        text-white 
        border border-red-700  /* Borde rojo para consistencia */
        
        /* ESTADO HOVER: Fondo rojo más oscuro (red-800) */
        hover:bg-red-800 
        hover:border-red-800  /* Oscurecemos el borde también */
        
        /* FORMATO */
        px-3 py-3 rounded-md text-sm
        transition-colors duration-200
        inline-flex items-center justify-center /* Alineación para la lupa */
    "
>
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
</button>
      
      
      
      
      
        <!-- 
        <button
          @click="goToSites"
          class="bg-transparent text-red-700 border border-red-700 hover:bg-transparent hover:text-gray-900 hover:border-gray-900 px-4 py-2 rounded-md text-sm transition-colors duration-200"
        >
          Buscar
        </button>
      -->
      


        <div v-if="isLoggedIn" class="relative hidden md:block">
          <button @click="toggleMenu" class="desktop-btn flex items-center gap-2">
            <img v-if="user?.picture" :src="user.picture" class="w-8 h-8 rounded-full object-cover" />
            <span>{{ user?.nombre || user?.email }}</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>

          <transition name="fade">
            <div 
              v-if="menuOpen" 
              class="desktop-menu absolute right-0 mt-2 w-48 bg-white text-black rounded-lg shadow-lg overflow-hidden z-50 flex flex-col divide-y">
              <router-link to="/perfil" class="menu-item block px-4 py-3 hover:bg-gray-100" @click="toggleMenu">Perfil</router-link>
              <router-link to="/mis-resenas" class="menu-item block px-4 py-3 hover:bg-gray-100" @click="toggleMenu">Mis reseñas</router-link>
              <router-link to="/favoritos" class="menu-item block px-4 py-3 hover:bg-gray-100" @click="toggleMenu">Sitios favoritos</router-link>
              <button @click="handleLogout" class="menu-item block px-4 py-3 hover:bg-gray-100 text-red-600 hover:bg-red-50">
                Cerrar sesión
              </button>
            </div>
          </transition>
        </div>
        
        <div v-else class="hidden md:block">
          <GoogleLoginButton @logged-in="handleLoginSuccess" />
        </div>
      </div>
    </div>

    <!-- MENU MOBILE -->

    <transition name="fade">
      <div 
        v-if="mobileMenuOpen && !isMaintenance"
        class="mobile-menu md:hidden absolute top-full left-1/2 transform -translate-x-1/2 mt-3 bg-white text-black rounded-lg shadow-lg p-4 z-50 w-[92vw] max-w-xs">

        <router-link to="/sitios" @click="closeMobileMenu" class="mobile-item">Buscar</router-link>
        <template v-if="isLoggedIn">
          <router-link to="/perfil" @click="closeMobileMenu" class="mobile-item">Perfil</router-link>
          <router-link to="/mis-resenas" @click="closeMobileMenu" class="mobile-item">Mis reseñas</router-link>
          <router-link to="/favoritos" @click="closeMobileMenu" class="mobile-item">Sitios favoritos</router-link>
          <button @click="handleLogout" class="mobile-item text-red-500">
            Cerrar sesión</button>
        </template>
        <template v-else>
          <GoogleLoginButton @logged-in="handleLoginSuccess" class="mobile-item" />
        </template>
      </div>
    </transition>

  </header>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import { useRouter } from "vue-router"
import GoogleLoginButton from "@/components/login_google/login.vue"
import { useSystemStore } from "@/stores/system"

const router = useRouter()
const system = useSystemStore()


const isMaintenance = computed(() => system.maintenance?.maintenance === true)

const isLoggedIn = ref(false)
const user = ref(null)
const menuOpen = ref(false)
const mobileMenuOpen = ref(false)

const toggleMenu = () => (menuOpen.value = !menuOpen.value)
const closeMobileMenu = () => (mobileMenuOpen.value = false)

function handleOutsideClick(e) {
  const btn = e.target.closest(".desktop-btn")
  const menu = e.target.closest(".desktop-menu")
  if (!btn && !menu) menuOpen.value = false
}

onMounted(() => {
  document.addEventListener("click", handleOutsideClick)

  const savedUser = localStorage.getItem("user")
  const savedToken = localStorage.getItem("token")

  if (savedUser && savedToken) {
    user.value = JSON.parse(savedUser)
    isLoggedIn.value = true
  }
})

onBeforeUnmount(() => {
  document.removeEventListener("click", handleOutsideClick)
})

const handleLoginSuccess = ({ user: u, token }) => {
  user.value = u
  isLoggedIn.value = true
  localStorage.setItem("user", JSON.stringify(u))
  localStorage.setItem("token", token)
}

const handleLogout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("user")
  user.value = null
  isLoggedIn.value = false
  window.location.reload();
 
}

const goToSites = () => router.push("/sitios")
const goToHome = () => router.push("/")
</script>


<style scoped>

</style>

<style scoped>

.header-container {
  background-color: #ece8e8; /* #333 es un gris oscuro*/
  padding: 15px 0px 12px 16px;
  color: #000;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: center;
  width: 100%;
  box-sizing: border-box;
}

.header-content {
  display: flex;
  align-items: stretch;
  justify-content: center;
  max-width: 100%;
  gap: 12px;
  width: 100%;
  gap: 0;
}

.logo-and-social {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

@media (min-width: 768px) {
  .logo-and-social {
    flex-direction: row;
    align-items: center;
  }
  .socials {
    margin-left: 12px;
    margin-top: 0;
  }
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0px;
  gap: 10px;
}

.logo-img {
  height: 50px;
}

.logo-img {
  object-fit: contain;
  width: auto;
}

@media (min-width: 768px) {
  .logo-img {
    height: 70px; /* Ajusta el tamaño según sea necesario */
  width: auto;
  }
}

.separator-bar {
  width: 6px;
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
  display: block;
  color: rgb(107,106,106);
}

.social-btn:hover {
  color: rgb(169,17,20);
}

.social-desktop {
  margin-left: 12px;
}

.hamburger {
  margin-left: auto;
  font-size: 1.6rem;
  background: transparent;
  border: none;
}

.menu-desktop {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-search {
  background: transparent;
  color: #b91c1c; /* red-700 */
  border: 1px solid #b91c1c;
  padding: 8px 12px;
  border-radius: 6px;
}

.desktop-btn {
  background: #111827; /* gray-900 */
  color: #fff;
  padding: 8px 10px;
  border-radius: 8px;
}

.mobile-menu {
  width: 92vw;
  max-width: 320px;
}

.mobile-item {
  display: block;
  padding: 10px 12px;
  border-radius: 8px;
  background: #f3f3f3;
  text-align: left;
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
