import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import 'swiper/css'
import 'vue-sonner/style.css'
import router from './router'
import GoogleSignInPlugin from 'vue3-google-signin'

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID
const app = createApp(App)
app.use(router)
app.use(GoogleSignInPlugin, {
  clientId: GOOGLE_CLIENT_ID
})

app.mount('#app')
