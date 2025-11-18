import { createRouter, createWebHistory } from 'vue-router'
import SiteDetailView from '@/views/sites/site_detail.vue'
import Home from '../home.vue'
import { useSystemStore } from '@/stores/system'  // <-- agregado

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/sitios', name: 'sites-list', component: () => import('@/views/sites/sites_list.vue') },
  { path: '/sitio/:id', name: 'site-detail', component: SiteDetailView },
  { path: '/login', name: 'login', component: () => import('@/components/login_google/login.vue') },
  { path: '/map', name: 'map', component: () => import('@/views/MapView.vue')},
  {
    path: '/mis-resenas',
    name: 'my-reviews',
    component: () => import('@/views/profile/MyReviews.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'profile',
    component: () => import('@/views/profile/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favoritos',
    name: 'favorites',
    component: () => import('@/views/profile/FavoriteSites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/maintenance',
    name: 'maintenance',
    component: () => import('@/views/maintenance/maintenance.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  const system = useSystemStore()

  // cargar estado de mantenimiento si aún no se cargó
  if (!system.loaded) {
    await system.loadStatus()
  }


 if (system.maintenance?.maintenance === true) {
  if (to.path !== '/maintenance') {
    return next('/maintenance')
  }
}


  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  next()
})

export default router
