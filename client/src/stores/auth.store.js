// client/src/stores/auth.store.js
import { defineStore } from 'pinia'
import api from '@/api/http'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userName: (state) => state.user ? state.user.full_name : 'Гость'
  },

  actions: {
    async login(email, password) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.post('/auth/login', { email, password })
        this.token = response.data.access_token
        localStorage.setItem('access_token', this.token)
        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка входа'
        return false
      } finally {
        this.isLoading = false
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        const response = await api.get('/users/me')
        this.user = response.data
      } catch (err) {
        console.error('Failed to fetch user:', err)
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    },

    async init() {
      if (this.token) {
        await this.fetchUser()
      }
    }
  }
})