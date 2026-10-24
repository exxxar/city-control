// client/src/services/offline.service.js
import { storageService } from './storage.service'
import api from '@/api/http'

class OfflineService {
  constructor() {
    this.isOnline = navigator.onLine
    this.isSyncing = false

    window.addEventListener('online', () => this.handleOnline())
    window.addEventListener('offline', () => this.handleOffline())
  }

  handleOnline() {
    this.isOnline = true
    console.log('[OfflineService] Connection restored. Starting sync...')
    this.syncQueue()
  }

  handleOffline() {
    this.isOnline = false
    console.log('[OfflineService] Connection lost. Actions will be queued.')
  }

  async addToQueue(actionType, data, files = []) {
    const queueItem = {
      id: Date.now() + Math.random(),
      type: actionType,
      data,
      files, // Массив Blob/File объектов
      createdAt: new Date().toISOString(),
      attempts: 0,
      status: 'pending'
    }

    // Сохраняем данные в IndexedDB (чтобы поддержать файлы)
    await storageService.saveToIndexedDB('offline_queue', queueItem)
    console.log('[OfflineService] Added to queue:', actionType)
    return queueItem.id
  }

  async getQueue() {
    return await storageService.getAllFromIndexedDB('offline_queue')
  }

  async syncQueue() {
    if (!this.isOnline || this.isSyncing) return

    this.isSyncing = true
    const queue = await this.getQueue()
    const pendingItems = queue.filter(item => item.status === 'pending')

    for (const item of pendingItems) {
      try {
        await this.processItem(item)
        await storageService.deleteFromIndexedDB('offline_queue', item.id)
        console.log('[OfflineService] Synced item:', item.id)
      } catch (err) {
        console.error('[OfflineService] Sync failed for item:', item.id, err)
        item.attempts += 1
        if (item.attempts >= 3) {
          item.status = 'failed'
          await storageService.saveToIndexedDB('offline_queue', item)
        }
      }
    }

    this.isSyncing = false
  }

  async processItem(item) {
    switch (item.type) {
      case 'create_problem':
        await this.syncCreateProblem(item.data, item.files)
        break
      case 'send_message':
        await this.syncSendMessage(item.data)
        break
      case 'confirm_problem':
        await this.syncConfirmProblem(item.data)
        break
      default:
        console.warn('[OfflineService] Unknown action type:', item.type)
    }
  }

  async syncCreateProblem(data, files) {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      formData.append(key, data[key])
    })

    files.forEach((file, index) => {
      formData.append(`files[${index}]`, file)
    })

    await api.post('/problems', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }

  async syncSendMessage(data) {
    await api.post(`/problems/${data.problemId}/messages`, { content: data.content })
  }

  async syncConfirmProblem(data) {
    await api.post(`/problems/${data.problemId}/confirmations`)
  }

  async retryItem(itemId) {
    const item = await storageService.getFromIndexedDB('offline_queue', itemId)
    if (item) {
      item.status = 'pending'
      item.attempts = 0
      await storageService.saveToIndexedDB('offline_queue', item)
      if (this.isOnline) this.syncQueue()
    }
  }

  async clearQueue() {
    const queue = await this.getQueue()
    for (const item of queue) {
      await storageService.deleteFromIndexedDB('offline_queue', item.id)
    }
  }
}

export const offlineService = new OfflineService()