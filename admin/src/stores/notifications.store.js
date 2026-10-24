// admin/src/stores/notifications.store.js
import { defineStore } from 'pinia'
import { notificationsApi } from '@/api/notifications.api'

export const useNotificationsStore = defineStore('notifications', {
    state: () => ({
        items: [],
        isLoading: false,
        isUsingMock: false
    }),

    getters: {
        unreadCount: (state) => state.items.filter(n => !n.is_read).length,
        unreadItems: (state) => state.items.filter(n => !n.is_read)
    },

    actions: {
        async fetchNotifications() {
            this.isLoading = true
            try {
                try {
                    this.items = await notificationsApi.getAll()
                    this.isUsingMock = false
                } catch {
                    this.items = await notificationsApi.getMockNotifications()
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        },

        async markAsRead(id) {
            try {
                await notificationsApi.markAsRead(id)
                const item = this.items.find(n => n.id === id)
                if (item) item.is_read = true
            } catch (error) {
                console.error('Mark as read error:', error)
            }
        },

        async markAllAsRead() {
            try {
                await notificationsApi.markAllAsRead()
                this.items.forEach(n => n.is_read = true)
            } catch (error) {
                console.error('Mark all as read error:', error)
            }
        }
    }
})