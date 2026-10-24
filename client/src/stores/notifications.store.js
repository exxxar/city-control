// client/src/stores/notifications.store.js
import { defineStore } from 'pinia'
import * as notificationsApi from '@/api/notifications.api'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    isLoading: false,
    error: null
  }),

  getters: {
    unreadNotifications: (state) => {
      return state.notifications.filter(n => !n.is_read)
    },

    recentNotifications: (state) => {
      return state.notifications.slice(0, 10)
    }
  },

  actions: {
    async fetchNotifications(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await notificationsApi.getNotifications(params)
        this.notifications = response.items || response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка загрузки уведомлений'
        console.error('Failed to fetch notifications:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchUnreadCount() {
      try {
        const response = await notificationsApi.getUnreadCount()
        this.unreadCount = response.count || 0
      } catch (err) {
        console.error('Failed to fetch unread count:', err)
      }
    },

    async markAsRead(notificationIds) {
      try {
        await notificationsApi.markNotificationsAsRead(notificationIds)

        notificationIds.forEach(id => {
          const notif = this.notifications.find(n => n.id === id)
          if (notif) {
            notif.is_read = true
          }
        })

        this.unreadCount = Math.max(0, this.unreadCount - notificationIds.length)
      } catch (err) {
        console.error('Failed to mark as read:', err)
      }
    },

    async markAllAsRead() {
      try {
        await notificationsApi.markAllAsRead()

        this.notifications.forEach(n => {
          n.is_read = true
        })

        this.unreadCount = 0
      } catch (err) {
        console.error('Failed to mark all as read:', err)
      }
    },

    addNotification(notification) {
      this.notifications.unshift(notification)
      if (!notification.is_read) {
        this.unreadCount += 1
      }
    },

    clearError() {
      this.error = null
    }
  }
})