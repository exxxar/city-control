// client/src/stores/user.store.js
import { defineStore } from 'pinia'
import api from '@/api/http'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.profile,
    fullName: (state) => state.profile?.full_name || 'Гость',
    email: (state) => state.profile?.email || '',
    roles: (state) => state.profile?.roles || [],
    hasRole: (state) => (roleName) => {
      return state.profile?.roles?.some(r => r.name === roleName) || false
    }
  },

  actions: {
    async fetchProfile() {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.get('/users/me')
        this.profile = response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки профиля'
        console.error('Failed to fetch profile:', err)
      } finally {
        this.isLoading = false
      }
    },

    async updateProfile(data) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.patch('/users/me', data)
        this.profile = response.data
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка обновления профиля'
        return false
      } finally {
        this.isLoading = false
      }
    },

    clearProfile() {
      this.profile = null
      this.error = null
    }
  }
})