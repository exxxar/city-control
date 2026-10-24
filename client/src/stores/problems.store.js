// client/src/stores/problems.store.js
import { defineStore } from 'pinia'
import * as problemsApi from '@/api/problems.api'

export const useProblemsStore = defineStore('problems', {
  state: () => ({
    problems: [],
    currentProblem: null,
    myProblems: [],
    filters: {
      status: null,
      category_id: null,
      territory_id: null,
      page: 1,
      per_page: 50
    },
    pagination: {
      total: 0,
      page: 1,
      per_page: 50,
      pages: 0
    },
    isLoading: false,
    isLoadingMore: false,
    error: null
  }),

  getters: {
    problemsByStatus: (state) => (status) => {
      return state.problems.filter(p => p.status === status)
    },
    activeProblems: (state) => {
      return state.problems.filter(p =>
        !['resolved', 'closed', 'rejected'].includes(p.status)
      )
    },
    problemById: (state) => (id) => {
      return state.problems.find(p => p.id === id) || state.currentProblem
    }
  },

  actions: {
    async fetchProblems(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await problemsApi.getProblems({
          ...this.filters,
          ...params
        })

        if (params.page === 1) {
          this.problems = response.items || response
        } else {
          this.problems = [...this.problems, ...(response.items || response)]
        }

        if (response.total !== undefined) {
          this.pagination = {
            total: response.total,
            page: response.page,
            per_page: response.per_page,
            pages: response.pages
          }
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки проблем'
        console.error('Failed to fetch problems:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchMyProblems() {
      this.isLoading = true
      this.error = null
      try {
        const response = await problemsApi.getMyProblems()
        this.myProblems = response.items || response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки моих проблем'
        console.error('Failed to fetch my problems:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchProblem(problemId) {
      this.isLoading = true
      this.error = null
      try {
        const response = await problemsApi.getProblem(problemId)
        this.currentProblem = response
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки проблемы'
        console.error('Failed to fetch problem:', err)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async createProblem(problemData) {
      this.isLoading = true
      this.error = null
      try {
        const response = await problemsApi.createProblem(problemData)
        this.problems.unshift(response)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка создания проблемы'
        console.error('Failed to create problem:', err)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    async updateProblem(problemId, updateData) {
      this.isLoading = true
      this.error = null
      try {
        const response = await problemsApi.updateProblem(problemId, updateData)

        const index = this.problems.findIndex(p => p.id === problemId)
        if (index !== -1) {
          this.problems[index] = response
        }

        if (this.currentProblem?.id === problemId) {
          this.currentProblem = response
        }

        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка обновления проблемы'
        console.error('Failed to update problem:', err)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    async changeStatus(problemId, newStatus, comment = null) {
      try {
        const response = await problemsApi.changeProblemStatus(problemId, newStatus, comment)

        const index = this.problems.findIndex(p => p.id === problemId)
        if (index !== -1) {
          this.problems[index].status = newStatus
        }

        if (this.currentProblem?.id === problemId) {
          this.currentProblem.status = newStatus
        }

        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка изменения статуса'
        console.error('Failed to change status:', err)
        throw err
      }
    },

    async confirmProblem(problemId) {
      try {
        const response = await problemsApi.confirmProblem(problemId)

        const index = this.problems.findIndex(p => p.id === problemId)
        if (index !== -1) {
          this.problems[index].confirmations_count += 1
        }

        if (this.currentProblem?.id === problemId) {
          this.currentProblem.confirmations_count += 1
        }

        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка подтверждения проблемы'
        console.error('Failed to confirm problem:', err)
        throw err
      }
    },

    async findSimilarProblems(params) {
      try {
        const response = await problemsApi.findSimilarProblems(params)
        return response
      } catch (err) {
        console.error('Failed to find similar problems:', err)
        return []
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    resetFilters() {
      this.filters = {
        status: null,
        category_id: null,
        territory_id: null,
        page: 1,
        per_page: 50
      }
    },

    clearCurrentProblem() {
      this.currentProblem = null
    },

    clearError() {
      this.error = null
    }
  }
})