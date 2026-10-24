// admin/src/stores/reports.store.js
import { defineStore } from 'pinia'
import { reportsApi } from '@/api/reports.api'

export const useReportsStore = defineStore('reports', {
    state: () => ({
        reports: [],
        isLoading: false,
        pagination: { page: 1, per_page: 20, pages: 0, total: 0 },
        isUsingMock: false
    }),

    getters: {
        pendingCount: (state) => state.reports.filter(r => r.status === 'pending').length,
        approvedCount: (state) => state.reports.filter(r => r.status === 'approved').length,
        rejectedCount: (state) => state.reports.filter(r => r.status === 'rejected').length,
        revisionCount: (state) => state.reports.filter(r => r.status === 'revision').length
    },

    actions: {
        async fetchReports(params = {}) {
            this.isLoading = true
            try {
                try {
                    const response = await reportsApi.getAll(params)
                    this.reports = response.items || response
                    this.pagination = {
                        page: response.page || 1,
                        per_page: response.per_page || 20,
                        pages: response.pages || 0,
                        total: response.total || 0
                    }
                    this.isUsingMock = false
                } catch {
                    const response = await reportsApi.getMockReports(params)
                    this.reports = response.items || response
                    this.pagination = {
                        page: response.page || 1,
                        per_page: response.per_page || 20,
                        pages: response.pages || 0,
                        total: response.total || 0
                    }
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        },

        async approveReport(id) {
            try {
                await reportsApi.approve(id)
                const report = this.reports.find(r => r.id === id)
                if (report) report.status = 'approved'
                return true
            } catch (error) {
                console.error('Approve error:', error)
                throw error
            }
        },

        async rejectReport(id, reason) {
            try {
                await reportsApi.reject(id, reason)
                const report = this.reports.find(r => r.id === id)
                if (report) report.status = 'rejected'
                return true
            } catch (error) {
                console.error('Reject error:', error)
                throw error
            }
        },

        async requestRevision(id, comment) {
            try {
                await reportsApi.requestRevision(id, comment)
                const report = this.reports.find(r => r.id === id)
                if (report) report.status = 'revision'
                return true
            } catch (error) {
                console.error('Revision error:', error)
                throw error
            }
        }
    }
})