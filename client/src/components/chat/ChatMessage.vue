<!-- client/src/components/chat/ChatMessage.vue -->
<template>
  <div :class="['chat-message d-flex gap-2 mb-3', { 'flex-row-reverse': isMine }]">
    <div class="avatar bg-light rounded-circle d-flex align-items-center justify-content-center flex-shrink-0">
      <IconFa name="person" size="1.25rem" color="#6c757d" />
    </div>

    <div :class="['message-bubble p-3 rounded-3', { 'bg-civic text-white': isMine, 'bg-light': !isMine }]">
      <div v-if="!isMine" class="fw-bold small mb-1">{{ message.user?.full_name || 'Пользователь' }}</div>
      <p class="mb-1">{{ message.content }}</p>
      <small :class="['text-end d-block', isMine ? 'text-white-50' : 'text-muted']" style="font-size: 0.7rem;">
        {{ formatTime(message.created_at) }}
      </small>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useAuthStore } from '@/stores/auth.store'

export default {
  name: 'ChatMessage',
  components: { IconFa },
  props: {
    message: { type: Object, required: true }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    isMine() {
      return this.message.user_id === this.authStore.user?.id
    }
  },
  methods: {
    formatTime(date) {
      if (!date) return ''
      return new Date(date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.avatar {
  width: 40px;
  height: 40px;
}

.message-bubble {
  max-width: 70%;
  word-wrap: break-word;
}

.bg-civic {
  background: linear-gradient(135deg, #00A896, #007EA7) !important;
}
</style>