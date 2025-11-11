import { createRouter, createWebHistory } from 'vue-router'
import SiteDetailView from '@/views/sites/site_detail.vue'
import Home from '../home.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sitios', name: 'sites-list', component: () => import('@/views/sites/sites_list.vue') },
  { path: '/sitio/:id', name: 'site-detail', component: SiteDetailView },
  { path: '/login', name: 'login', component: () => import('@/components/login_google/login.vue') },
  {
    path: '/mis-resenas',
    name: 'my-reviews',
    component: () => import('@/views/profile/MyReviews.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
