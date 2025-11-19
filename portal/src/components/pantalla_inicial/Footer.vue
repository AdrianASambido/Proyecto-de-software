<template>
  <footer class="bg-gray-500 text-white p-6 w-full my-4">
    <div class="container mx-auto px-4">
      <div class="flex flex-wrap justify-between">
        <!-- Columna de Contacto -->
        <div class="w-full md:w-1/3 mb-6 md:mb-0">
          <h4 class="text-lg font-semibold mb-2">Contacto</h4>
          <p class="text-sm mb-1">Calle 50 y 118, La Plata, Argentina</p>
          <p class="text-sm mb-1">
            <a href="tel:+541112345678" class="hover:text-teal-400">(+54) 11 1234-5678</a>
          </p>
          <p class="text-sm">
            <a href="mailto:contacto@mi-proyecto.com" class="hover:text-teal-400">contacto@mi-proyecto.com</a>
          </p>
        </div>

        <!-- Columna de Redes Sociales -->
        <div class="w-full md:w-1/3 mb-6 md:mb-0">
          <h4 class="text-lg font-semibold mb-2">Redes Sociales</h4>
          <div class="flex items-center gap-4">
            <a href="#" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" class="text-white hover:text-teal-400">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M4.98 3.5C4.98 4.88 3.86 6 2.48 6S0 4.88 0 3.5 1.12 1 2.5 1 4.98 2.12 4.98 3.5zM.24 8h4.48V24H.24V8zM8.24 8h4.3v2.16h.06c.6-1.14 2.07-2.34 4.26-2.34C22.1 7.82 24 10.2 24 14.2V24h-4.5v-8.1c0-1.93-.04-4.42-2.7-4.42-2.72 0-3.14 2.12-3.14 4.3V24H8.24V8z"/>
              </svg>
            </a>
            <a href="#" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="text-white hover:text-teal-400">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M22 12.07C22 6.48 17.52 2 11.93 2S2 6.48 2 12.07C2 17.09 5.66 21.19 10.44 21.93v-6.99H7.9v-2.87h2.54V9.41c0-2.5 1.49-3.87 3.77-3.87 1.09 0 2.23.2 2.23.2v2.45h-1.25c-1.23 0-1.61.77-1.61 1.56v1.87h2.74l-.44 2.87h-2.3V21.93C18.34 21.19 22 17.09 22 12.07z"/>
              </svg>
            </a>
            <a href="#" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="text-white hover:text-teal-400">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 2.16c3.2 0 3.584.012 4.85.07 1.17.056 1.96.24 2.42.4.6.22 1.03.48 1.48.93.45.45.71.88.93 1.48.16.46.344 1.25.4 2.42.058 1.265.07 1.65.07 4.85s-.012 3.584-.07 4.85c-.056 1.17-.24 1.96-.4 2.42-.22.6-.48 1.03-.93 1.48-.45.45-.88.71-1.48.93-.46.16-1.25.344-2.42.4-1.265.058-1.65.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.056-1.96-.24-2.42-.4-.6-.22-1.03-.48-1.48-.93-.45-.45-.71-.88-.93-1.48-.16-.46-.344-1.25-.4-2.42C2.172 15.584 2.16 15.2 2.16 12s.012-3.584.07-4.85c.056-1.17.24-1.96.4-2.42.22-.6.48-1.03.93-1.48.45-.45.88-.71 1.48-.93.46-.16 1.25-.344 2.42-.4C8.416 2.172 8.8 2.16 12 2.16zm0 1.84c-3.13 0-3.496.012-4.73.068-1.02.05-1.58.22-1.95.366-.5.19-.86.416-1.24.794-.38.38-.604.74-.794 1.24-.146.37-.316.93-.366 1.95C2.172 8.504 2.16 8.87 2.16 12s.012 3.496.068 4.73c.05 1.02.22 1.58.366 1.95.19.5.416.86.794 1.24.38.38.74.604 1.24.794.37.146.93.316 1.95.366 1.234.056 1.6.068 4.73.068s3.496-.012 4.73-.068c1.02-.05 1.58-.22 1.95-.366.5-.19.86-.416 1.24-.794.38-.38.604-.74.794-1.24.146-.37.316-.93.366-1.95.056-1.234.068-1.6.068-4.73s-.012-3.496-.068-4.73c-.05-1.02-.22-1.58-.366-1.95-.19-.5-.416-.86-.794-1.24-.38-.38-.74-.604-1.24-.794-.37-.146-.93-.316-1.95-.366C15.496 4.016 15.13 4.004 12 4.004zM12 7.2a4.8 4.8 0 110 9.6 4.8 4.8 0 010-9.6zm0 1.92a2.88 2.88 0 100 5.76 2.88 2.88 0 000-5.76zm5.1-2.58a1.12 1.12 0 11-2.24 0 1.12 1.12 0 012.24 0z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Columna de Enlaces -->
        <div class="w-full md:w-1/3">
          <h4 class="text-lg font-semibold mb-2">Enlaces</h4>
          <ul>
            <li class="mb-1"><a href="#" class="hover:text-teal-400">Favoritos</a></li>
            <li class="mb-1"><a href="#" class="hover:text-teal-400">Recientemente Agregados</a></li>
            <li><a href="#" class="hover:text-teal-400">Imágenes Destacadas</a></li>
          </ul>
        </div>
      </div>
      <div class="mt-6 text-center">
        <p>&copy; {{ new Date().getFullYear() }} Mi Proyecto. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>
