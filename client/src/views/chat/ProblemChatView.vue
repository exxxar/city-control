<!-- client/src/views/chat/ProblemChatView.vue -->
<template>
  <div class="problem-chat-view d-flex flex-column" style="height: 100vh;">
    <!-- Header -->
    <div class="chat-header bg-white border-bottom p-3 d-flex align-items-center gap-3">
      <button class="btn btn-link text-secondary p-0" @click="$router.back()">
        <IconFa name="arrow-left" size="1.5rem" />
      </button>
      <div class="flex-grow-1">
        <h6 class="mb-0 fw-bold">Чат проблемы</h6>
        <small class="text-muted">{{ problem?.title }}</small>
      </div>
      <UiBadge :variant="statusVariant" size="sm">
        {{ statusText }}
      </UiBadge>
    </div>

    <!-- Messages -->
    <div ref="messagesContainer" class="chat-messages flex-grow-1 overflow-auto p-3 bg-light">
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-civic"></div>
      </div>

      <div v-else-if="messages.length === 0" class="text-center py-5">
        <IconFa name="chat-dots" size="3rem" color="#adb5bd" />
        <p class="text-muted mt-3">Нет сообщений</p>
      </div>

      <div v-else>
        <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message"
        />
      </div>
    </div>

    <!-- Input -->
    <ChatInput
      :is-sending="isSending"
      @send="sendMessage"
    />
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import ChatMessage from '@/components/chat/ChatMessage.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import { useChatStore } from '@/stores/chat.store'
import { useProblemsStore } from '@/stores/problems.store'
import { usePusher } from '@/composables/usePusher'

export default {
  name: 'ProblemChatView',
  components: { IconFa, UiBadge, ChatMessage, ChatInput },
  props: {
    id: { type: [String, Number], required: true }
  },
  data() {
    return {
      isLoading: false,
      isSending: false
    }
  },
  computed: {
    chatStore() {
      return useChatStore()
    },
    problemsStore() {
      return useProblemsStore()
    },
    problem() {
      return this.problemsStore.currentProblem
    },
    messages() {
      return this.chatStore.messages
    },
    statusVariant() {
      const status = this.problem?.status
      const map = {
        'new': 'secondary', 'in_progress': 'warning', 'resolved': 'success'
      }
      return map[status] || 'secondary'
    },
    statusText() {
      const status = this.problem?.status
      const map = {
        'new': 'Новая', 'in_progress': 'В работе', 'resolved': 'Устранена'
      }
      return map[status] || status
    }
  },
  async mounted() {
    await this.loadChat()
    this.initRealtime()
  },
  beforeUnmount() {
    this.chatStore.clearMessages()
  },
  methods: {
    async loadChat() {
      this.isLoading = true
      try {
        await Promise.all([
          this.problemsStore.fetchProblem(this.id),
          this.chatStore.fetchMessages(this.id)
        ])
        this.scrollToBottom()
      } catch (error) {
        console.error('Failed to load chat:', error)
      } finally {
        this.isLoading = false
      }
    },

    initRealtime() {
      const { subscribeToProblemChannel } = usePusher()
      subscribeToProblemChannel(this.id, (data) => {
        if (data.type === 'new_message') {
          this.chatStore.addMessage(data.message)
          this.scrollToBottom()
        }
      })
    },

    async sendMessage(content) {
      this.isSending = true
      try {
        await this.chatStore.sendMessage(this.id, content)
        this.scrollToBottom()
      } catch (error) {
        console.error('Failed to send message:', error)
        alert('Ошибка отправки сообщения')
      } finally {
        this.isSending = false
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.chat-messages {
  scroll-behavior: smooth;
}
</style>