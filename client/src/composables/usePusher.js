// client/src/composables/usePusher.js
import { ref, onMounted, onUnmounted } from 'vue'
import Pusher from 'pusher-js'
import { useAuthStore } from '@/stores/auth.store'
import { useNotificationsStore } from '@/stores/notifications.store'

export function usePusher() {
  const authStore = useAuthStore()
  const notificationsStore = useNotificationsStore()

  const pusher = ref(null)
  const channels = ref({})
  const isConnected = ref(false)

  function init() {
    if (pusher.value || !authStore.isAuthenticated) return

    pusher.value = new Pusher(import.meta.env.VITE_PUSHER_KEY, {
      cluster: import.meta.env.VITE_PUSHER_CLUSTER,
      authEndpoint: '/api/pusher/auth',
      auth: {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    })

    pusher.value.connection.bind('connected', () => {
      isConnected.value = true
      console.log('Pusher connected')
    })

    pusher.value.connection.bind('disconnected', () => {
      isConnected.value = false
      console.log('Pusher disconnected')
    })

    pusher.value.connection.bind('error', (err) => {
      console.error('Pusher error:', err)
    })
  }

  function subscribe(channelName, eventName, callback) {
    if (!pusher.value) return

    if (!channels.value[channelName]) {
      channels.value[channelName] = pusher.value.subscribe(channelName)
    }

    const channel = channels.value[channelName]
    channel.bind(eventName, callback)

    return () => {
      channel.unbind(eventName, callback)
    }
  }

  function subscribeToUserChannel(userId, callback) {
    return subscribe(`private-user-${userId}`, 'notification.new', callback)
  }

  function subscribeToProblemChannel(problemId, callback) {
    return subscribe(`private-problem-${problemId}`, 'problem.updated', callback)
  }

  function unsubscribe(channelName) {
    if (!pusher.value || !channels.value[channelName]) return
    pusher.value.unsubscribe(channelName)
    delete channels.value[channelName]
  }

  function destroy() {
    if (pusher.value) {
      Object.keys(channels.value).forEach(channelName => {
        unsubscribe(channelName)
      })
      pusher.value.disconnect()
      pusher.value = null
      isConnected.value = false
    }
  }

  onMounted(() => {
    if (authStore.isAuthenticated) {
      init()
    }
  })

  onUnmounted(() => {
    destroy()
  })

  return {
    pusher,
    isConnected,
    init,
    subscribe,
    subscribeToUserChannel,
    subscribeToProblemChannel,
    unsubscribe,
    destroy
  }
}