// client/src/composables/useNotifications.js
import { computed, onMounted } from 'vue'
import { useNotificationsStore } from '@/stores/notifications.store'
import { usePusher } from './usePusher'
import { useAuthStore } from '@/stores/auth.store'

export function useNotifications() {
  const notificationsStore = useNotificationsStore()
  const authStore = useAuthStore()
  const { subscribeToUserChannel } = usePusher()

  const notifications = computed(() => notificationsStore.notifications)
  const unreadCount = computed(() => notificationsStore.unreadCount)
  const isLoading = computed(() => notificationsStore.isLoading)

  async function fetchNotifications(params = {}) {
    await notificationsStore.fetchNotifications(params)
  }

  async function markAsRead(notificationIds) {
    await notificationsStore.markAsRead(notificationIds)
  }

  async function markAllAsRead() {
    await notificationsStore.markAllAsRead()
  }

  function initRealtime() {
    if (!authStore.user) return

    subscribeToUserChannel(authStore.user.id, (data) => {
      notificationsStore.addNotification(data.notification)
    })
  }

  onMounted(() => {
    if (authStore.isAuthenticated) {
      fetchNotifications()
      initRealtime()
    }
  })

  return {
    notifications,
    unreadCount,
    isLoading,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    initRealtime
  }
}