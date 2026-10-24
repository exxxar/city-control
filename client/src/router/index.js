// client/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import { setupGuards } from './guards'

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.meta.scrollToTop === false) {
      return false
    } else {
      return { top: 0 }
    }
  }
})

// Устанавливаем guard'ы
setupGuards(router)

export default router