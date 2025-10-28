<template>
  <header class="header-container">
    <div class="header-content">
      <h1 class="logo">Portal Histórico</h1>
      <div class="buscador-rapido">
        <input type="text" placeholder="Buscar..." class="input-busqueda">
        <button class="btn-busqueda">🔍</button>
      </div>
      <div>
        <button class="btn-busqueda" href="">Login con Google</button>
      </div>
    </div>
  </header>
</template>

<script setup>
  // acá que iria??
  import LoginGoogle from "../login_google/login.vue";
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