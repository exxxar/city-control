// client/src/composables/useAuth.js
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.store'

export function useAuth() {
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const currentUser = computed(() => authStore.user)
  const userRoles = computed(() => authStore.user?.roles || [])

  // Просто возвращаем результат, а роутинг оставляем компоненту
  async function login(email, password) {
    return await authStore.login(email, password)
  }

  function logout() {
    authStore.logout()
  }

  async function register(userData) {
    return await authStore.register(userData)
  }

  function hasRole(roleName) {
    return userRoles.value.some(r => r.name === roleName)
  }

  function hasAnyRole(roleNames) {
    return roleNames.some(role => hasRole(role))
  }

  return {
    isAuthenticated,
    currentUser,
    userRoles,
    login,
    logout,
    register,
    hasRole,
    hasAnyRole
  }
}