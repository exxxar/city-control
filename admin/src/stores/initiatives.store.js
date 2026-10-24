// admin/src/stores/initiatives.store.js
import { defineStore } from 'pinia'
import { initiativesApi } from '@/api/initiatives.api'

export const useInitiativesStore = defineStore('initiatives', {
    state: () => ({
        initiatives: [],
        isLoading: false,
        pagination: { page: 1, per_page: 20, pages: 0, total: 0 },
        isUsingMock: false
    }),

    getters: {
        pendingCount: (state) => state.initiatives.filter(i => i.status === 'pending').length,
        implementedCount: (state) => state.initiatives.filter(i => i.status === 'implemented').length
    },

    actions: {
        async fetchInitiatives(params = {}) {
            this.isLoading = true
            try {
                // Пытаемся получить данные из админского API
                const response = await initiativesApi.getAll(params)

                this.initiatives = response.items || response
                this.pagination = {
                    page: response.page || 1,
                    per_page: response.per_page || 20,
                    pages: response.pages || 0,
                    total: response.total || 0
                }
                this.isUsingMock = false
            } catch (error) {
                console.warn('Admin API failed, falling back to mock or showing empty', error)
                // Если API еще не готов, можно раскомментировать мок, но с новым роутом он должен работать
                this.isUsingMock = true
            } finally {
                this.isLoading = false
            }
        },

        async approveInitiative(id) {
            await initiativesApi.approve(id)
            const item = this.initiatives.find(i => i.id === id)
            if (item) item.status = 'approved'
        },

        async rejectInitiative(id, reason) {
            await initiativesApi.reject(id, reason)
            const item = this.initiatives.find(i => i.id === id)
            if (item) {
                item.status = 'rejected'
                item.reject_reason = reason
            }
        },

        async implementInitiative(id) {
            await initiativesApi.implement(id)
            const item = this.initiatives.find(i => i.id === id)
            if (item) item.status = 'implemented'
        }
    }
})