<template>
  <section v-if="isAuthenticated" class="container mx-auto p-4 md:p-8 mt-8">
    <GaleriaTarjetasMonumentos
      :items="items"
      :loading="loading"
      :error="error"
      title="Mis Favoritos"
      :view-all-route="viewAllRoute"
      empty-message="No tienes sitios favoritos. ¡Explora y agrega algunos!"
    />
  </section>
  
  <section v-else class="container mx-auto p-4 md:p-8 mt-8">
  <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
    <svg class="mx-auto h-12 w-12 text-blue-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
    <h3 class="text-lg font-semibold text-gray-900 mb-2">
      Inicia sesión para ver tus favoritos
    </h3>
    <p class="text-gray-600 mb-4">
      Guarda tus sitios históricos favoritos y accede a ellos fácilmente.
    </p>
    <button
      @click="showLoginPopup = true"
      class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
    >
      Iniciar sesión con Google
    </button>
  </div>

  <!-- Popup reutilizable -->
  <LoginPopup v-model="showLoginPopup" @login="onLoginSuccess" />
</section>

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import GaleriaTarjetasMonumentos from './galeriaTarjetasMonumentos.vue'
import { useSites } from '@/composables/useSites'
import { useAuth } from '@/composables/useAuth'
import LoginPopup from '@/components/login_google/loginPopUp.vue'

const router = useRouter()
const { isAuthenticated, currentUser } = useAuth()
const { loading, error, fetchFavoritos } = useSites()
const items = ref([])

// Ruta para "Ver todos" con el filtro de favoritos aplicado
const viewAllRoute = computed(() => {
  if (!isAuthenticated.value) return null
  return fetchFavoritos;
})
const showLoginPopup = ref(false)

const onLoginSuccess = (user) => {
  showLoginPopup.value = false
  // después del login, recargamos los favoritos
  loadData()
}

// Carga perezosa solo si está autenticado
const loadData = async () => {
  if (!isAuthenticated.value || loading.value || items.value.length > 0) return
  
  // Intentamos cargar favoritos. El backend puede obtener el user_id del token/sesión
  // Si el backend requiere user_id explícito, currentUser.value?.id debería tenerlo
  const data = await fetchFavoritos(currentUser.value?.id || null)
  items.value = data
}

// Observar cambios en autenticación
watch(isAuthenticated, (newVal) => {
  if (newVal) {
    loadData()
  } else {
    items.value = []
  }
})

onMounted(() => {
  if (isAuthenticated.value) {
    loadData()
  }
})
</script>

