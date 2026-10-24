<!-- client/src/components/chat/ChatInput.vue -->
<template>
  <div class="chat-input-container bg-white border-top p-3">
    <form @submit.prevent="sendMessage" class="d-flex gap-2">
      <input
        v-model="messageText"
        type="text"
        class="form-control"
        placeholder="Написать сообщение..."
        :disabled="isSending"
      >
      <button type="submit" class="btn btn-civic" :disabled="!messageText.trim() || isSending">
        <IconFa :name="isSending ? 'hourglass-split' : 'send'" />
      </button>
    </form>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'ChatInput',
  components: { IconFa },
  props: {
    isSending: { type: Boolean, default: false }
  },
  emits: ['send'],
  data() {
    return {
      messageText: ''
    }
  },
  methods: {
    sendMessage() {
      if (!this.messageText.trim()) return
      this.$emit('send', this.messageText)
      this.messageText = ''
    }
  }
}
</script>

<style scoped>
.btn-civic {
  background: var(--civic-primary, #00A896);
  color: white;
  border: none;
}
</style>