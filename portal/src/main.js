import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import 'swiper/css'
import 'vue-sonner/style.css'
import router from './router'
import axios from 'axios'
import { createPinia } from 'pinia'
import GoogleSignInPlugin from 'vue3-google-signin'


axios.defaults.baseURL = import.meta.env.VITE_BASE_URL

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID
const app = createApp(App)

app.use(router)
app.use(createPinia())
app.use(GoogleSignInPlugin, {
  clientId: GOOGLE_CLIENT_ID
})


app.mount('#app')
