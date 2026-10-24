// client/src/stores/offlineQueue.store.js
import { defineStore } from 'pinia'

const QUEUE_KEY = 'offline_queue'
const SYNC_STATUS_KEY = 'sync_status'

export const useOfflineQueueStore = defineStore('offlineQueue', {
  state: () => ({
    queue: JSON.parse(localStorage.getItem(QUEUE_KEY) || '[]'),
    isOnline: navigator.onLine,
    isSyncing: false,
    lastSyncTime: localStorage.getItem(SYNC_STATUS_KEY) || null
  }),

  getters: {
    pendingItems: (state) => {
      return state.queue.filter(item => item.status === 'pending')
    },

    failedItems: (state) => {
      return state.queue.filter(item => item.status === 'failed')
    },

    queueLength: (state) => state.queue.length
  },

  actions: {
    addToQueue(item) {
      const queueItem = {
        id: Date.now() + Math.random(),
        ...item,
        status: 'pending',
        createdAt: new Date().toISOString(),
        attempts: 0
      }

      this.queue.push(queueItem)
      this.saveToLocalStorage()
    },

    async processQueue() {
      if (this.isSyncing || !this.isOnline) return

      this.isSyncing = true

      for (const item of this.pendingItems) {
        try {
          await this.syncItem(item)
          this.removeItem(item.id)
        } catch (err) {
          console.error('Failed to sync item:', item, err)
          item.attempts += 1

          if (item.attempts >= 3) {
            item.status = 'failed'
          }

          this.saveToLocalStorage()
        }
      }

      this.lastSyncTime = new Date().toISOString()
      localStorage.setItem(SYNC_STATUS_KEY, this.lastSyncTime)
      this.isSyncing = false
    },

    async syncItem(item) {
      // Здесь будет логика отправки в зависимости от типа действия
      // Например, для создания проблемы:
      if (item.type === 'create_problem') {
        const { createProblem } = await import('@/api/problems.api')
        await createProblem(item.data)
      }
      // Добавить другие типы действий
    },

    removeItem(itemId) {
      this.queue = this.queue.filter(item => item.id !== itemId)
      this.saveToLocalStorage()
    },

    retryItem(itemId) {
      const item = this.queue.find(i => i.id === itemId)
      if (item) {
        item.status = 'pending'
        item.attempts = 0
        this.saveToLocalStorage()
      }
    },

    clearQueue() {
      this.queue = []
      this.saveToLocalStorage()
    },

    saveToLocalStorage() {
      localStorage.setItem(QUEUE_KEY, JSON.stringify(this.queue))
    },

    setOnlineStatus(isOnline) {
      this.isOnline = isOnline
      if (isOnline) {
        this.processQueue()
      }
    },

    init() {
      window.addEventListener('online', () => this.setOnlineStatus(true))
      window.addEventListener('offline', () => this.setOnlineStatus(false))

      if (this.isOnline && this.queue.length > 0) {
        this.processQueue()
      }
    }
  }
})