<template>
  <footer class="bg-gray-800 text-white p-6 max-w-screen-lg mx-auto rounded-lg my-4">
    <div class="container mx-auto px-4 flex flex-col items-center justify-center">

      <div class="text-center">
        <h4 class="text-lg font-semibold mb-2">Contacto</h4>
        
        <p class="text-sm flex items-center justify-center mb-1">
          <span class="mr-2"></span> 
          Calle 50 y 118, Ciudad La Plata, Argentina
        </p>
        
        <p class="text-sm flex items-center justify-center mb-1">
          <span class="mr-2"></span>
          <a href="tel:+541112345678" class="hover:text-teal-400">(+54) 11 1234-5678</a>
        </p>
        
        <p class="text-sm flex items-center justify-end">
          <span class="mr-2">✉️</span>
          <a href="mailto:contacto@mi-proyecto.com" class="hover:text-teal-400">contacto@mi-proyecto.com</a>
        </p>
      </div>
      <div class="mb-4 text-center">
        <p>&copy; {{ new Date().getFullYear() }} Mi Proyecto. Todos los derechos reservados.</p>
        </div>
      </div>
  </footer>
</template>
