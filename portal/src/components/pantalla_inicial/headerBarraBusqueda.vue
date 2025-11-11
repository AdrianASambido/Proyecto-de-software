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
        <div v-if="isLoggedIn" class="user-info">
          <span class="username">Hola, {{ username }}</span>
          <button @click="handleLogout" class="btn-logout">Cerrar sesión</button>
        </div>

        <div v-else>
          <GoogleLoginButton @logged-in="handleLoginSuccess" />
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import GoogleLoginButton from '@/components/login_google/login.vue'

const router = useRouter()
const isLoggedIn = ref(false)
const username = ref('')

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  const savedToken = localStorage.getItem('token')
  if (savedUser && savedToken) {
    username.value = JSON.parse(savedUser).nombre || JSON.parse(savedUser).email
    isLoggedIn.value = true
  }
})

const goToSites = () => {
  router.push('/sitios')
}

const handleLoginSuccess = (user) => {
  username.value = user.nombre || user.email
  isLoggedIn.value = true
  console.log('Usuario logueado:', user)
}

const handleLogout = async () => {


  isLoggedIn.value = false
  username.value = ''
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  window.location.reload()
  console.log('Sesión cerrada exitosamente')
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
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-busqueda:hover {
  background-color: #0056b3;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  color: white;
  font-size: 0.95em;
  font-weight: 500;
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-logout:hover {
  background-color: #c82333;
}
</style>
