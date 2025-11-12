<template>
  <div>
    <div ref="googleButton"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const emit = defineEmits(["logged-in"])
const BASE_URL = import.meta.env.VITE_BASE_URL || "https://admin-grupo01.proyecto2025.linti.unlp.edu.ar/api"
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "156550318843-bag3rvvvo3kquesgsgdrr8f6j4p0nmv4.apps.googleusercontent.com"
const googleButton = ref(null)

onMounted(() => {
  const script = document.createElement("script")
  script.src = "https://accounts.google.com/gsi/client"
  script.async = true
  script.defer = true
  script.onload = initializeGoogleButton
  document.head.appendChild(script)
})

function initializeGoogleButton() {
  window.google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
  })

  window.google.accounts.id.renderButton(googleButton.value, {
    theme: "outline",
    size: "medium",
    text: "signin_with",
    shape: "pill",
  })
}

async function handleCredentialResponse(response) {
  try {
    const id_token = response.credential

    const res = await axios.post(BASE_URL + "/login/google", {
      id_token,
    })

    const { token, user } = res.data

    localStorage.setItem("token", token)
    localStorage.setItem("user", JSON.stringify(user))
    window.location.reload()
 
    emit("logged-in", user)
  } catch (error) {
    console.error("Error en login con Google:", error)
    alert("Error al iniciar sesión con Google")
  }
}
</script>
