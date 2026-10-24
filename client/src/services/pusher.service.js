// client/src/services/pusher.service.js
import Pusher from 'pusher-js'

class PusherService {
  constructor() {
    this.pusher = null
    this.channels = {}
    this.isConnected = false
  }

  init(options = {}) {
    if (this.pusher) return

    const key = import.meta.env.VITE_PUSHER_KEY
    const cluster = import.meta.env.VITE_PUSHER_CLUSTER || 'eu'

    if (!key) {
      console.warn('[PusherService] VITE_PUSHER_KEY is not set. Real-time updates disabled.')
      return
    }

    this.pusher = new Pusher(key, {
      cluster,
      authEndpoint: '/api/pusher/auth',
      auth: {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      },
      ...options
    })

    this.pusher.connection.bind('connected', () => {
      this.isConnected = true
      console.log('[PusherService] Connected')
    })

    this.pusher.connection.bind('disconnected', () => {
      this.isConnected = false
      console.log('[PusherService] Disconnected')
    })

    this.pusher.connection.bind('error', (err) => {
      console.error('[PusherService] Connection error:', err)
    })
  }

  subscribe(channelName, eventName, callback) {
    if (!this.pusher) return null

    if (!this.channels[channelName]) {
      this.channels[channelName] = this.pusher.subscribe(channelName)
    }

    const channel = this.channels[channelName]
    channel.bind(eventName, callback)

    // Возвращаем функцию для отписки
    return () => {
      channel.unbind(eventName, callback)
    }
  }

  subscribeToUser(userId, callback) {
    return this.subscribe(`private-user-${userId}`, 'notification.new', callback)
  }

  subscribeToProblem(problemId, callback) {
    return this.subscribe(`private-problem-${problemId}`, 'problem.updated', callback)
  }

  unsubscribe(channelName) {
    if (!this.pusher || !this.channels[channelName]) return
    this.pusher.unsubscribe(channelName)
    delete this.channels[channelName]
  }

  destroy() {
    if (!this.pusher) return

    Object.keys(this.channels).forEach(channelName => {
      this.unsubscribe(channelName)
    })

    this.pusher.disconnect()
    this.pusher = null
    this.isConnected = false
  }

  updateAuthToken(token) {
    if (this.pusher) {
      this.pusher.config.auth.headers.Authorization = `Bearer ${token}`
    }
  }
}

export const pusherService = new PusherService()