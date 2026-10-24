// client/src/stores/initiatives.store.js
import { defineStore } from 'pinia'
import * as initiativesApi from '@/api/initiatives.api'

export const useInitiativesStore = defineStore('initiatives', {
  state: () => ({
    initiatives: [],
    currentInitiative: null,
    filters: {
      status: null,
      page: 1,
      per_page: 20
    },
    pagination: {
      total: 0,
      page: 1,
      per_page: 20,
      pages: 0
    },
    isLoading: false,
    error: null
  }),

  getters: {
    activeInitiatives: (state) => {
      return state.initiatives.filter(i =>
        !['rejected', 'completed'].includes(i.status)
      )
    }
  },

  actions: {
    async fetchInitiatives(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await initiativesApi.getInitiatives({
          ...this.filters,
          ...params
        })

        this.initiatives = response.items || response

        if (response.total !== undefined) {
          this.pagination = {
            total: response.total,
            page: response.page,
            per_page: response.per_page,
            pages: response.pages
          }
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки инициатив'
        console.error('Failed to fetch initiatives:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchInitiative(initiativeId) {
      this.isLoading = true
      this.error = null
      try {
        const response = await initiativesApi.getInitiative(initiativeId)
        this.currentInitiative = response
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки инициативы'
        console.error('Failed to fetch initiative:', err)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async createInitiative(data) {
      this.isLoading = true
      this.error = null
      try {
        const response = await initiativesApi.createInitiative(data)
        this.initiatives.unshift(response)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка создания инициативы'
        console.error('Failed to create initiative:', err)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    async supportInitiative(initiativeId) {
      try {
        const response = await initiativesApi.supportInitiative(initiativeId)

        const index = this.initiatives.findIndex(i => i.id === initiativeId)
        if (index !== -1) {
          this.initiatives[index].support_count = response.total
        }

        if (this.currentInitiative?.id === initiativeId) {
          this.currentInitiative.support_count = response.total
        }

        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка поддержки инициативы'
        console.error('Failed to support initiative:', err)
        throw err
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    clearCurrentInitiative() {
      this.currentInitiative = null
    },

    clearError() {
      this.error = null
    }
  }
})