<template>
  <header class="header-container">
    <div class="header-content">
      <h1 class="logo">Portal Histórico</h1>
      <div class="buscador-rapido"><!--Que será este error-->
        <input v-model="searchTerm" type="text" placeholder="Buscar..." class="input-busqueda" @keyup.enter="performSearch">
        <button class="btn-busqueda" @click="performSearch">🔍</button>
      </div>
      <div class="auth-section">
        <!-- Mostrar información del usuario y botón de cerrar sesión si está logueado -->
        <div v-if="isLoggedIn" class="user-info">
          <span class="username">Hola, {{ username }}</span>
          <button @click="handleLogout" class="btn-logout">Cerrar sesión</button>
        </div>
        <!-- Mostrar botón de login si no está logueado -->
        <div v-else>
          <GoogleSignInButton @success="handleLoginSuccess" @error="handleLoginError"></GoogleSignInButton>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
  import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
  import { ref, onMounted } from 'vue';
  import api from '@/api/axios';

  // Declaración de tipos para window.google
  declare global {
    interface Window {
      google?: {
        accounts: {
          id: {
            disableAutoSelect: () => void;
          };
        };
      };
    }
  }
  
  const isLoggedIn = ref(false);
  const username = ref('');
  const searchTerm = ref('');

  // Verificar si hay sesión guardada al cargar el componente
  onMounted(() => {
    const savedUsername = localStorage.getItem('google_username');
    const savedLoginState = localStorage.getItem('google_logged_in');
    if (savedUsername && savedLoginState === 'true') {
      username.value = savedUsername;
      isLoggedIn.value = true;
    }
  });

  const emit = defineEmits<{
    (e: 'search', searchTerm: string): void;
  }>();

  const performSearch = () => {
    emit('search', searchTerm.value);
  };

  const handleLoginError = (error: any) => {
    console.error('Error de inicio de sesión:', error);
  };

  const handleLoginSuccess = (response: CredentialResponse) => {
    const idToken = response.credential;
    console.log('Inicio de sesión exitoso. ID Token:', idToken);

    try {
      const payload = JSON.parse(atob(idToken.split('.')[1]));
      username.value = payload.name || '';
      isLoggedIn.value = true;

      // Guardar el estado de sesión en localStorage
      localStorage.setItem('google_username', username.value);
      localStorage.setItem('google_logged_in', 'true');
      localStorage.setItem('google_token', idToken);

      console.log('Nombre de usuario:', username.value);
    } catch (error) {
      console.error('Error al procesar el token:', error);
    }
  };

  const handleLogout = async () => {
    try {
      // Llamar al endpoint de logout del backend
      await api.post('/logout');
    } catch (error) {
      console.error('Error al cerrar sesión en el backend:', error);
      // Continuar con el logout local aunque falle el backend
    }

    // Limpiar el estado local
    isLoggedIn.value = false;
    username.value = '';
    
    // Limpiar localStorage
    localStorage.removeItem('google_username');
    localStorage.removeItem('google_logged_in');
    localStorage.removeItem('google_token');
    localStorage.removeItem('auth_token');

    // Intentar revocar la sesión de Google
    if (window.google && window.google.accounts) {
      window.google.accounts.id.disableAutoSelect();
    }

    console.log('Sesión cerrada exitosamente');
  };
</script>

<style scoped>
/* Estilos para la barra horizontal en la cabecera */
.header-container {
  background-color: #333; /* Fondo oscuro */
  padding: 15px 20px;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex; /* Para centrar contenido si es necesario */
  justify-content: center; /* Centra horizontalmente */
  width: 100%; /* Ocupa todo el ancho */
  box-sizing: border-box; /* Incluye padding en el ancho */
}

.header-content {
  display: flex;
  justify-content: space-between; /* Espacia el logo y el buscador */
  align-items: center; /* Alinea verticalmente */
  max-width: 1200px; /* Ancho máximo del contenido */
  width: 100%;
}

.logo {
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
}

.buscador-rapido {
  display: flex;
  gap: 5px; /* Espacio entre input y botón */
}

.input-busqueda {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  width: 200px; /* Ancho del input */
}

.btn-busqueda {
  background-color: #007bff; /* Color de botón azul */
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
}

.btn-busqueda:hover {
  background-color: #0056b3; /* Oscurecer al pasar el ratón */
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
  background-color: #dc3545; /* Color rojo para el botón de cerrar sesión */
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
  background-color: #c82333; /* Oscurecer al pasar el ratón */
}
</style>
