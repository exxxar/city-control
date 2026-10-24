// client/src/stores/chat.store.js
import { defineStore } from 'pinia'
import * as messagesApi from '@/api/messages.api'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [],
    currentProblemId: null,
    isLoading: false,
    isLoadingMore: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      per_page: 50,
      pages: 0
    }
  }),

  getters: {
    sortedMessages: (state) => {
      return [...state.messages].sort((a, b) =>
        new Date(a.created_at) - new Date(b.created_at)
      )
    },

    lastMessage: (state) => {
      if (state.messages.length === 0) return null
      return state.sortedMessages[state.sortedMessages.length - 1]
    }
  },

  actions: {
    async fetchMessages(problemId, params = {}) {
      this.currentProblemId = problemId
      this.isLoading = true
      this.error = null
      try {
        const response = await messagesApi.getMessages(problemId, {
          page: 1,
          per_page: 50,
          ...params
        })

        this.messages = response.items || response

        if (response.total !== undefined) {
          this.pagination = {
            total: response.total,
            page: response.page,
            per_page: response.per_page,
            pages: response.pages
          }
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки сообщений'
        console.error('Failed to fetch messages:', err)
      } finally {
        this.isLoading = false
      }
    },

    async loadMoreMessages(problemId) {
      if (this.pagination.page >= this.pagination.pages) return

      this.isLoadingMore = true
      try {
        const nextPage = this.pagination.page + 1
        const response = await messagesApi.getMessages(problemId, {
          page: nextPage,
          per_page: this.pagination.per_page
        })

        this.messages = [...(response.items || response), ...this.messages]
        this.pagination.page = nextPage
      } catch (err) {
        console.error('Failed to load more messages:', err)
      } finally {
        this.isLoadingMore = false
      }
    },

    async sendMessage(problemId, content) {
      try {
        const response = await messagesApi.sendMessage(problemId, content)
        this.messages.push(response)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка отправки сообщения'
        console.error('Failed to send message:', err)
        throw err
      }
    },

    addMessage(message) {
      this.messages.push(message)
    },

    clearMessages() {
      this.messages = []
      this.currentProblemId = null
      this.pagination = {
        total: 0,
        page: 1,
        per_page: 50,
        pages: 0
      }
    },

    clearError() {
      this.error = null
    }
  }
})