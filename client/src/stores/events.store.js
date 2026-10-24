// client/src/stores/events.store.js
import { defineStore } from 'pinia'
import * as eventsApi from '@/api/events.api'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [],
    currentEvent: null,
    isLoading: false,
    error: null,
    pagination: {
      page: 1,
      per_page: 20,
      pages: 0,
      total: 0
    }
  }),

  actions: {
    async fetchEvents(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await eventsApi.getEvents(params)
        this.events = response.items || response
        if (response.total !== undefined) {
          this.pagination = {
            page: response.page || 1,
            per_page: response.per_page || 20,
            pages: response.pages || 0,
            total: response.total || 0
          }
        }
        return this.events
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки мероприятий'
        console.error('Fetch events error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchEvent(id) {
      this.isLoading = true
      this.error = null
      try {
        const event = await eventsApi.getEvent(id)
        this.currentEvent = event
        return event
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка загрузки мероприятия'
        console.error('Fetch event error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createEvent(payload) {
      this.isLoading = true
      this.error = null
      try {
        // Если payload это FormData, axios обработает его автоматически
        const event = await eventsApi.createEvent(payload)
        this.events.unshift(event)
        return event
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка создания мероприятия'
        console.error('Create event error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    clearCurrentEvent() {
      this.currentEvent = null
    }
  }
})