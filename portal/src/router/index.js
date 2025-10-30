import { createRouter, createWebHistory } from 'vue-router'
import SiteDetailView from '@/views/sites/site_detail.vue'

const routes = [
  { path: '/sitio/:id', name: 'site-detail', component: SiteDetailView }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

