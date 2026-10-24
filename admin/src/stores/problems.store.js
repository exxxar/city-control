// admin/src/stores/problems.store.js
import { defineStore } from 'pinia'
import http from '@/api/http'

export const useProblemsStore = defineStore('problems', {
    state: () => ({
        problems: [],
        executors: [],
        isLoading: false,
        pagination: { page: 1, per_page: 20, pages: 0, total: 0 },
        isUsingMock: false
    }),

    getters: {
        newCount: (state) => state.problems.filter(p => p.status === 'new').length,
        inProgressCount: (state) => state.problems.filter(p => p.status === 'in_progress').length
    },

    actions: {
        async fetchProblems(params = {}) {
            this.isLoading = true
            try {
                const response = await http.get('/admin/problems', { params })
                this.problems = response.data.items || response.data
                this.pagination = {
                    page: response.data.page || 1,
                    per_page: response.data.per_page || 20,
                    pages: response.data.pages || 0,
                    total: response.data.total || 0
                }
                this.isUsingMock = false
            } catch (error) {
                console.error('Fetch problems error:', error)
                this.isUsingMock = true
            } finally {
                this.isLoading = false
            }
        },

        async fetchExecutors() {
            try {
                // Получаем пользователей и фильтруем тех, у кого роль "Исполнитель"
                const response = await http.get('/admin/users', { params: { per_page: 100 } })
                const users = response.data.items || response.data
                this.executors = users.filter(u => u.roles?.some(r => r.name === 'Исполнитель'))

                // Если исполнителей не нашли, добавляем заглушку для демонстрации
                if (this.executors.length === 0) {
                    this.executors = [
                        { id: 991, full_name: 'Козлова Мария Александровна (ЖКХ)' },
                        { id: 992, full_name: 'Смирнов Виктор Олегович (Дороги)' }
                    ]
                }
            } catch (error) {
                console.error('Fetch executors error:', error)
            }
        },

        async moderateProblem(id, status, rejectReason = '') {
            await http.post(`/admin/problems/${id}/moderate`, {
                status: status,
                reject_reason: rejectReason
            })
        },

        async assignProblem(id, executorId) {
            await http.post(`/admin/problems/${id}/assign`, {
                executor_id: executorId
            })
        }
    }
})