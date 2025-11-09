<template>
  <div class="google-login-container">
    <!-- Botón de Google (se renderiza aquí cuando está listo) -->
    <div ref="googleButton" class="google-button-wrapper"></div>
    
    <!-- Mensaje de error si no se puede cargar -->
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <p v-if="error.includes('no configurado')" class="error-hint">
        Por favor, configura VITE_GOOGLE_CLIENT_ID en el archivo .env
      </p>
    </div>
    
    <!-- Loading mientras se carga el script -->
    <div v-if="loading && !error" class="loading-message">
      <p>Cargando botón de inicio de sesión...</p>
    </div>
    
    <!-- Botón de fallback si Google no está disponible -->
    <button 
      v-if="error && error.includes('no disponible')" 
      @click="handleManualLogin"
      class="fallback-button"
    >
      Iniciar sesión
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import api from "@/api/axios"

const emit = defineEmits(["logged-in"])
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID
const googleButton = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  // Verificar si ya existe el script de Google
  const existingScript = document.querySelector('script[src="https://accounts.google.com/gsi/client"]')
  
  if (!GOOGLE_CLIENT_ID) {
    error.value = "Google Client ID no configurado"
    loading.value = false
    console.error("VITE_GOOGLE_CLIENT_ID no está configurado en las variables de entorno")
    return
  }

  // Si el script ya existe, intentar inicializar directamente
  if (existingScript) {
    if (window.google) {
      await nextTick()
      initializeGoogleButton()
    } else {
      // Esperar a que el script existente se cargue
      existingScript.onload = initializeGoogleButton
      // Si ya está cargado, intentar inicializar después de un pequeño delay
      setTimeout(() => {
        if (window.google) {
          initializeGoogleButton()
        } else {
          error.value = "Error al cargar Google Sign-In"
          loading.value = false
        }
      }, 1000)
    }
  } else {
    // Crear el script si no existe
    const script = document.createElement("script")
    script.src = "https://accounts.google.com/gsi/client"
    script.async = true
    script.defer = true
    script.onload = initializeGoogleButton
    script.onerror = () => {
      error.value = "Error al cargar el script de Google"
      loading.value = false
    }
    document.head.appendChild(script)
  }
})

function initializeGoogleButton() {
  try {
    if (!window.google) {
      error.value = "Google Sign-In no disponible"
      loading.value = false
      console.error("Google Sign-In script no se cargó correctamente")
      return
    }

    if (!GOOGLE_CLIENT_ID) {
      error.value = "Google Client ID no configurado"
      loading.value = false
      return
    }

    window.google.accounts.id.initialize({
      client_id: GOOGLE_CLIENT_ID,
      callback: handleCredentialResponse,
    })

    // Esperar a que el DOM esté listo antes de renderizar el botón
    nextTick(() => {
      if (googleButton.value) {
        try {
          window.google.accounts.id.renderButton(googleButton.value, {
            theme: "outline",
            size: "medium",
            text: "signin_with",
            shape: "pill",
          })
          loading.value = false
        } catch (err) {
          console.error("Error al renderizar el botón de Google:", err)
          error.value = "Error al mostrar el botón de inicio de sesión"
          loading.value = false
        }
      } else {
        // Si el ref no está listo, intentar de nuevo después de un delay
        setTimeout(() => {
          if (googleButton.value) {
            try {
              window.google.accounts.id.renderButton(googleButton.value, {
                theme: "outline",
                size: "medium",
                text: "signin_with",
                shape: "pill",
              })
              loading.value = false
            } catch (err) {
              console.error("Error al renderizar el botón de Google:", err)
              error.value = "Error al mostrar el botón de inicio de sesión"
              loading.value = false
            }
          } else {
            error.value = "Error al inicializar el botón"
            loading.value = false
          }
        }, 500)
      }
    })
  } catch (err) {
    console.error("Error en initializeGoogleButton:", err)
    error.value = "Error al inicializar Google Sign-In"
    loading.value = false
  }
}

async function handleCredentialResponse(response) {
  try {
    if (!response || !response.credential) {
      console.error("Respuesta de Google inválida:", response)
      alert("Error: No se recibió el token de Google")
      return
    }

    const id_token = response.credential
    console.log("Enviando token al backend...")

    const res = await api.post("/login/google", {
      id_token: id_token,
    })

    if (!res.data || !res.data.token) {
      console.error("Respuesta del backend inválida:", res.data)
      alert("Error: El servidor no devolvió un token válido")
      return
    }

    const { token, user } = res.data

    localStorage.setItem("token", token)
    localStorage.setItem("user", JSON.stringify(user))
    
    emit("logged-in", user)
    
    // Recargar la página para actualizar el estado de autenticación
    window.location.reload()
  } catch (error) {
    console.error("Error completo en login con Google:", error)
    console.error("Error response:", error.response?.data)
    console.error("Error status:", error.response?.status)
    
    const errorMessage = error.response?.data?.error || error.response?.data?.details || error.message || "Error desconocido al iniciar sesión con Google"
    alert(`Error al iniciar sesión: ${errorMessage}`)
  }
}

// Función de fallback si Google no está disponible
function handleManualLogin() {
  alert("Por favor, configura VITE_GOOGLE_CLIENT_ID en el archivo .env para habilitar el inicio de sesión con Google")
}
</script>

<style scoped>
.google-login-container {
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.google-button-wrapper {
  min-height: 40px;
  min-width: 200px;
}

.error-message {
  padding: 8px 12px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
  font-size: 0.9em;
}

.loading-message {
  padding: 8px 12px;
  color: #666;
  font-size: 0.9em;
}

.error-hint {
  margin-top: 4px;
  font-size: 0.85em;
  font-style: italic;
}

.fallback-button {
  padding: 8px 16px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  font-weight: 500;
}

.fallback-button:hover {
  background-color: #357ae8;
}
</style>
