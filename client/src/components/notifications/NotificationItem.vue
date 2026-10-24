<!-- client/src/components/notifications/NotificationItem.vue -->
<template>
  <div :class="['notification-item p-3 border-bottom', { 'bg-light': !notification.is_read }]" @click="$emit('click', notification)">
    <div class="d-flex gap-3">
      <div :class="['notif-icon rounded-circle d-flex align-items-center justify-content-center flex-shrink-0', `bg-${variant}`]">
        <IconFa :name="icon" size="1rem" color="white" />
      </div>

      <div class="flex-grow-1 min-w-0">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <strong class="small">{{ notification.title }}</strong>
          <small class="text-muted text-nowrap ms-2">{{ formatTimeAgo(notification.created_at) }}</small>
        </div>
        <p class="text-muted small mb-0 text-truncate">{{ notification.body }}</p>
      </div>

      <div v-if="!notification.is_read" class="unread-dot bg-danger rounded-circle align-self-center"></div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'NotificationItem',
  components: { IconFa },
  props: {
    notification: { type: Object, required: true }
  },
  emits: ['click'],
  computed: {
    variant() {
      const map = {
        'status_change': 'primary',
        'new_message': 'info',
        'sla_warning': 'danger',
        'geo_zone_entry': 'warning',
        'system': 'secondary'
      }
      return map[this.notification.type] || 'secondary'
    },
    icon() {
      const map = {
        'status_change': 'arrow-repeat',
        'new_message': 'chat-dots',
        'sla_warning': 'exclamation-triangle',
        'geo_zone_entry': 'geo-alt',
        'system': 'gear'
      }
      return map[this.notification.type] || 'bell'
    }
  },
  methods: {
    formatTimeAgo(date) {
      if (!date) return ''
      const diff = Date.now() - new Date(date).getTime()
      const minutes = Math.floor(diff / 60000)

      if (minutes < 60) return `${minutes} мин`
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours} ч`
      const days = Math.floor(hours / 24)
      return `${days} д`
    }
  }
}
</script>

<style scoped>
.notification-item {
  cursor: pointer;
  transition: background 0.2s;
}

.notification-item:hover {
  background: #f8f9fa;
}

.notif-icon {
  width: 40px;
  height: 40px;
}

.unread-dot {
  width: 8px;
  height: 8px;
}
</style>