// admin/src/stores/auth.store.js
import { defineStore } from 'pinia'
import { authApi } from '@/api/auth.api'

const ADMIN_ROLES = [
    'Системный администратор',
    'Руководитель органа',
    'Модератор'
]

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('admin_token') || null,
        isLoading: false,
        error: null
    }),

    getters: {
        isAuthenticated: (state) => !!state.token && !!state.user,
        userRoles: (state) => state.user?.roles || [],
        hasAdminAccess: (state) => {
            if (!state.user?.roles) return false
            return state.user.roles.some(r => ADMIN_ROLES.includes(r.name))
        },
        fullName: (state) => state.user?.full_name || 'Администратор',
        primaryRole: (state) => state.user?.roles?.[0]?.name || 'Администратор'
    },

    actions: {
        async login(email, password) {
            this.isLoading = true
            this.error = null
            try {
                const response = await authApi.login(email, password)
                this.token = response.access_token
                localStorage.setItem('admin_token', this.token)

                // Получаем данные пользователя
                await this.fetchUser()

                // Проверяем, есть ли у пользователя доступ к админке
                if (!this.hasAdminAccess) {
                    this.logout()
                    throw new Error('У вас нет прав доступа к админ-панели')
                }

                return true
            } catch (error) {
                this.logout()
                const message = error.response?.data?.detail || error.message || 'Ошибка входа'
                this.error = message
                throw new Error(message)
            } finally {
                this.isLoading = false
            }
        },

        async fetchUser() {
            if (!this.token) return
            try {
                this.user = await authApi.me()
            } catch (error) {
                this.logout()
                throw error
            }
        },

        async restoreSession() {
            if (!this.token || this.user) return
            try {
                await this.fetchUser()
                if (!this.hasAdminAccess) {
                    this.logout()
                }
            } catch {
                this.logout()
            }
        },

        logout() {
            this.user = null
            this.token = null
            this.error = null
            localStorage.removeItem('admin_token')
        },

        clearError() {
            this.error = null
        }
    }
})