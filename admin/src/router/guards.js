// admin/src/router/guards.js
import { useAuthStore } from '@/stores/auth.store'

export function setupGuards(router) {
    router.beforeEach(async (to, from, next) => {
        const authStore = useAuthStore()

        // Восстанавливаем сессию из токена при первой загрузке
        if (authStore.token && !authStore.user) {
            await authStore.restoreSession()
        }

        // Публичные страницы (только логин)
        if (to.meta.guestOnly) {
            if (authStore.isAuthenticated) {
                return next('/dashboard')
            }
            return next()
        }

        // Защищённые страницы
        if (to.meta.requiresAuth) {
            if (!authStore.isAuthenticated) {
                return next({ path: '/login', query: { redirect: to.fullPath } })
            }

            // Проверка ролей
            if (to.meta.roles) {
                const userRoles = authStore.userRoles.map(r => r.name)
                const hasAccess = to.meta.roles.some(role => userRoles.includes(role))
                if (!hasAccess) {
                    return next('/forbidden')
                }
            }
        }

        next()
    })
}