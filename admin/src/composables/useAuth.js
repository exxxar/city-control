import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useRouter } from 'vue-router'

export function useAuth() {
    const authStore = useAuthStore()
    const router = useRouter()

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentUser = computed(() => authStore.user)
    const userRoles = computed(() => authStore.user?.roles || [])

    const hasRole = (roleName) =>
        userRoles.value.some(r => r.name === roleName)

    const hasAnyRole = (roleNames) =>
        roleNames.some(role => hasRole(role))

    const isAdmin = computed(() =>
        hasRole('Системный администратор')
    )

    const isModerator = computed(() =>
        hasRole('Модератор') || hasRole('Системный администратор')
    )

    async function login(email, password) {
        await authStore.login(email, password)
        router.push('/dashboard')
    }

    function logout() {
        authStore.logout()
        router.push('/login')
    }

    return {
        isAuthenticated,
        currentUser,
        userRoles,
        isAdmin,
        isModerator,
        hasRole,
        hasAnyRole,
        login,
        logout
    }
}