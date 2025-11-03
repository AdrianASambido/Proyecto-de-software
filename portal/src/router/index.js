import { createRouter, createWebHistory } from 'vue-router'
import SiteDetailView from '@/views/sites/site_detail.vue'
import Home from '../home.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sitio/:id', name: 'site-detail', component: SiteDetailView },
  { path: '/login', name: 'login', component: () => import('@/components/login_google/login.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
