// client/src/router/guards.js
import { useAuthStore } from '@/stores/auth.store'

/**
 * Установка навигационных guard'ов
 * @param {Router} router - Экземпляр Vue Router
 */
export function setupGuards(router) {
  // === Глобальный before guard ===
  router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const isAuthenticated = authStore.isAuthenticated

    // Проверка требования авторизации
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

    // Проверка, что страница только для гостей (login, register)
    const guestOnly = to.matched.some(record => record.meta.guestOnly)

    // Если страница требует авторизации, но пользователь не залогинен
    if (requiresAuth && !isAuthenticated) {
      return next({
        name: 'Login',
        query: { redirect: to.fullPath }
      })
    }

    // Если страница только для гостей, но пользователь залогинен
    if (guestOnly && isAuthenticated) {
      return next({ name: 'Map' })
    }

    // Проверка ролей (если указаны в meta.roles)
    const requiredRoles = to.meta.roles
    if (requiredRoles && isAuthenticated) {
      const userRoles = authStore.user?.roles?.map(r => r.name) || []
      const hasRole = requiredRoles.some(role => userRoles.includes(role))

      if (!hasRole) {
        console.warn(`[Guard] Access denied. Required roles: ${requiredRoles.join(', ')}`)
        return next({ name: 'Map' }) // Или на страницу "Доступ запрещён"
      }
    }

    next()
  })

  // === После навигации (для аналитики, скролла и т.д.) ===
  router.afterEach((to, from) => {
    // Обновление заголовка страницы
    document.title = to.meta.title
      ? `${to.meta.title} | Город под контролем`
      : 'Город под контролем'

    // Прокрутка наверх при навигации (кроме сохранения позиции)
    if (to.meta.scrollToTop !== false) {
      window.scrollTo(0, 0)
    }

    // Логирование навигации (для аналитики)
    if (import.meta.env.DEV) {
      console.log(`[Router] ${from.name} → ${to.name}`)
    }
  })

  // === Обработка ошибок навигации ===
  router.onError((error, to, from) => {
    console.error('[Router] Navigation error:', error)

    // Если ошибка загрузки чанка (например, после деплоя новой версии)
    if (error.message.includes('Failed to fetch dynamically imported module')) {
      window.location.reload()
    }
  })
}

/**
 * Guard для проверки конкретных permissions
 * Используется внутри компонентов через composable usePermissions
 */
export function requirePermission(permission) {
  return (to, from, next) => {
    const authStore = useAuthStore()
    const userPermissions = authStore.user?.permissions || []

    if (userPermissions.includes(permission) || userPermissions.includes('admin.full_access')) {
      next()
    } else {
      console.warn(`[Guard] Permission denied: ${permission}`)
      next({ name: 'Map' })
    }
  }
}

/**
 * Guard для проверки, что пользователь является исполнителем
 */
export function requireExecutor(to, from, next) {
  const authStore = useAuthStore()
  const userRoles = authStore.user?.roles?.map(r => r.name) || []

  const executorRoles = ['Исполнитель', 'Руководитель органа', 'Системный администратор']
  const isExecutor = executorRoles.some(role => userRoles.includes(role))

  if (isExecutor) {
    next()
  } else {
    next({ name: 'Map' })
  }
}

export default setupGuards