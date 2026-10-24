// admin/src/stores/dashboard.store.js
import { defineStore } from 'pinia'
import { dashboardApi } from '@/api/dashboard.api'

export const useDashboardStore = defineStore('dashboard', {
    state: () => ({
        stats: {
            totalUsers: 0,
            totalProblems: 0,
            newProblems: 0,
            inProgressProblems: 0,
            resolvedProblems: 0,
            totalInitiatives: 0,
            totalEvents: 0,
            todayNewProblems: 0,
            weekNewProblems: 0
        },
        recentProblems: [],
        isLoading: false,
        error: null,
        isUsingMock: false // Флаг: используем ли заглушки
    }),

    getters: {
        resolutionRate: (state) => {
            if (!state.stats.totalProblems) return 0
            return Math.round((state.stats.resolvedProblems / state.stats.totalProblems) * 100)
        }
    },

    actions: {
        async fetchStats() {
            this.isLoading = true
            this.error = null
            try {
                // Пробуем реальный API, если упадёт — используем заглушку
                try {
                    this.stats = await dashboardApi.getStats()
                    this.isUsingMock = false
                } catch {
                    this.stats = await dashboardApi.getMockStats()
                    this.isUsingMock = true
                }
            } catch (error) {
                this.error = 'Не удалось загрузить статистику'
                console.error('Dashboard stats error:', error)
            } finally {
                this.isLoading = false
            }
        },

        async fetchRecentProblems(limit = 10) {
            try {
                try {
                    this.recentProblems = await dashboardApi.getRecentProblems(limit)
                } catch {
                    this.recentProblems = await dashboardApi.getMockRecentProblems()
                }
            } catch (error) {
                console.error('Recent problems error:', error)
            }
        },

        async loadAll() {
            await Promise.all([
                this.fetchStats(),
                this.fetchRecentProblems()
            ])
        }
    }
})