<template>
  <header class="header-container">
    <div class="header-content">
      <h1 class="logo">Portal Histórico</h1>
      <div class="buscador-rapido">
        <input type="text" placeholder="Buscar..." class="input-busqueda">
        <button class="btn-busqueda">🔍</button>
      </div>
      <div>
        <GoogleSignInButton @success="handleLoginSuccess" @error="handleLoginError"></GoogleSignInButton>
      </div>
      <div>
        <p>Logueado? {{ isLoggedIn ? 'Simón' : 'Nel pastel' }}</p>
        <p v-if="username">Usuario: {{ username }}</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
  import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
  import { ref } from 'vue';
  
  const isLoggedIn = ref(false); // Cambia esto según el estado de autenticación real
  const username = ref(''); // Cambia esto para mostrar el nombre de usuario real|

  const handleCredentialResponse = (response: CredentialResponse) => {
    console.log('ID Token:', response.credential);
    // Aquí puedes manejar la respuesta del inicio de sesión
  };

  const handleLoginError = (error: any) => {
    console.error('Error de inicio de sesión:', error);
  };

  const handleLoginSuccess = (response: CredentialResponse) => {
    const idToken = response.credential;
    console.log('Inicio de sesión exitoso. ID Token:', idToken);

    const payload = JSON.parse(atob(idToken.split('.')[1]));
    username.value = payload.name || '';
    isLoggedIn.value = true;

    console.log('Nombre de usuario:', username.value);
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
</style>