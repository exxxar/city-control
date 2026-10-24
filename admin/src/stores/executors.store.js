// admin/src/stores/executors.store.js
import { defineStore } from 'pinia'
import { executorsApi } from '@/api/executors.api'

export const useExecutorsStore = defineStore('executors', {
    state: () => ({
        stats: [],
        isLoading: false,
        isUsingMock: false
    }),

    getters: {
        topPerformers: (state) =>
            [...state.stats].sort((a, b) => b.rating - a.rating).slice(0, 3),

        totalCompleted: (state) =>
            state.stats.reduce((sum, e) => sum + e.completed, 0),

        avgRating: (state) => {
            if (!state.stats.length) return 0
            const sum = state.stats.reduce((acc, e) => acc + e.rating, 0)
            return (sum / state.stats.length).toFixed(1)
        }
    },

    actions: {
        async fetchStats() {
            this.isLoading = true
            try {
                try {
                    this.stats = await executorsApi.getStats()
                    this.isUsingMock = false
                } catch {
                    this.stats = await executorsApi.getMockStats()
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        }
    }
})