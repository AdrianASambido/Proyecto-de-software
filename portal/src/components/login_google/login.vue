<template>
  <div>
    <div ref="googleButton"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const emit = defineEmits(["logged-in"])
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID
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

    const res = await axios.post("http://localhost:5000/api/login/google", {
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
