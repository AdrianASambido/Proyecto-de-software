import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import 'swiper/css'
import router from './router'
import GoogleSignInPlugin from 'vue3-google-signin'

const app = createApp(App)

app.use(router)
app.use(GoogleSignInPlugin, {
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
})
app.mount('#app')
