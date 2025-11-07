import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import 'swiper/css'
import router from './router'
import GoogleSignInPlugin from 'vue3-google-signin'

const app = createApp(App)

app.use(router)
app.use(GoogleSignInPlugin, {
  clientId: '85082399211-189rlvpgbl0vsnt5fvhi7oi17ouhd8in.apps.googleusercontent.com'
})
app.mount('#app')
