// client/src/composables/usePermissions.js
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.store'

export function usePermissions() {
  const authStore = useAuthStore()

  const userPermissions = computed(() => {
    if (!authStore.user?.roles) return []
    const perms = new Set()
    authStore.user.roles.forEach(role => {
      role.permissions?.forEach(p => perms.add(p.codename))
    })
    return Array.from(perms)
  })

  function can(permission) {
    return userPermissions.value.includes(permission)
  }

  function canAny(permissions) {
    return permissions.some(p => can(p))
  }

  function canAll(permissions) {
    return permissions.every(p => can(p))
  }

  function isAdmin() {
    return can('admin.full_access')
  }

  function canCreateProblem() {
    return can('problem.create') || isAdmin()
  }

  function canModerate() {
    return can('problem.moderate') || isAdmin()
  }

  function canManageUsers() {
    return can('user.manage') || isAdmin()
  }

  return {
    userPermissions,
    can,
    canAny,
    canAll,
    isAdmin,
    canCreateProblem,
    canModerate,
    canManageUsers
  }
}