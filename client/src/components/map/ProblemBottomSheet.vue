<!-- client/src/components/map/ProblemBottomSheet.vue -->
<template>
  <UiBottomSheet
    :model-value="!!problem"
    @update:model-value="close"
    height="auto"
  >
    <template #header>
      <div class="d-flex align-items-start justify-content-between">
        <div class="flex-grow-1">
          <UiBadge :variant="statusVariant" size="sm" class="mb-2">
            {{ statusText }}
          </UiBadge>
          <h5 class="mb-1 fw-bold">{{ problem?.title }}</h5>
          <p class="text-muted small mb-0">{{ problem?.description }}</p>
        </div>
        <button class="btn btn-sm btn-link text-secondary" @click="close">
          <IconFa name="x-lg" />
        </button>
      </div>
    </template>

    <div class="problem-details">
      <!-- Meta info -->
      <div class="d-flex gap-3 mb-3 text-muted small">
        <div>
          <IconFa name="calendar3" size="0.875rem" class="me-1" />
          {{ formatDate(problem?.created_at) }}
        </div>
        <div>
          <IconFa name="chat-dots" size="0.875rem" class="me-1" />
          {{ problem?.messages_count || 0 }} сообщений
        </div>
        <div>
          <IconFa name="people" size="0.875rem" class="me-1" />
          {{ problem?.confirmations_count || 0 }} подтверждений
        </div>
      </div>

      <!-- Attachments preview -->
      <div v-if="problem?.attachments?.length > 0" class="attachments-preview mb-3">
        <div class="d-flex gap-2 overflow-auto">
          <img
            v-for="att in problem.attachments.slice(0, 3)"
            :key="att.id"
            :src="att.file_url"
            class="attachment-thumb rounded"
            alt="Вложение"
          >
        </div>
      </div>

      <!-- Actions -->
      <div class="d-flex gap-2">
        <router-link
          :to="`/problems/${problem?.id}/details`"
          class="btn btn-civic flex-grow-1"
        >
          <IconFa name="eye" class="me-2" />
          Открыть карточку
        </router-link>

        <button
          v-if="canConfirm"
          class="btn btn-outline-secondary"
          @click="confirmProblem"
        >
          <IconFa name="check2" />
        </button>
      </div>
    </div>
  </UiBottomSheet>
</template>

<script>
import UiBottomSheet from '@/components/ui/UiBottomSheet.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import IconFa from '@/components/ui/IconFa.vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'ProblemBottomSheet',
  components: { UiBottomSheet, UiBadge, IconFa },
  props: {
    problem: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'confirm'],
  setup() {
    const problemsStore = useProblemsStore()
    const { isAuthenticated } = useAuth()
    return { problemsStore, isAuthenticated }
  },
  computed: {
    statusVariant() {
      const status = this.problem?.status
      if (['new', 'needs_clarification'].includes(status)) return 'secondary'
      if (['confirmed', 'transferred', 'accepted'].includes(status)) return 'info'
      if (['in_progress', 'suspended'].includes(status)) return 'warning'
      if (['solution_ready', 'awaiting_confirmation'].includes(status)) return 'primary'
      if (['resolved', 'closed'].includes(status)) return 'success'
      if (status === 'rejected') return 'danger'
      return 'secondary'
    },
    statusText() {
      const statusMap = {
        'new': 'Новая',
        'needs_clarification': 'Требует уточнения',
        'confirmed': 'Подтверждена',
        'transferred': 'Передана',
        'accepted': 'Принята',
        'in_progress': 'В работе',
        'suspended': 'Приостановлена',
        'solution_ready': 'Решение готово',
        'awaiting_confirmation': 'Ожидает подтверждения',
        'resolved': 'Устранена',
        'closed': 'Закрыта',
        'rejected': 'Отклонена'
      }
      return statusMap[this.problem?.status] || 'Неизвестно'
    },
    canConfirm() {
      return this.isAuthenticated && this.problem?.status !== 'resolved' && this.problem?.status !== 'closed'
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    async confirmProblem() {
      try {
        await this.problemsStore.confirmProblem(this.problem.id)
        this.$emit('confirm', this.problem.id)
      } catch (err) {
        console.error('Failed to confirm problem:', err)
      }
    }
  }
}
</script>

<style scoped>
.problem-details {
  padding: 0.5rem 0;
}

.attachment-thumb {
  width: 80px;
  height: 80px;
  object-fit: cover;
  flex-shrink: 0;
}

.btn-civic {
  background: linear-gradient(135deg, #00A896, #007EA7);
  border: none;
  color: white;
}

.btn-civic:hover {
  background: linear-gradient(135deg, #008f80, #006a8a);
  color: white;
}
</style>