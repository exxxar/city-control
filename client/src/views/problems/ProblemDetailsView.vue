<!-- client/src/views/problems/ProblemDetailsView.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="d-flex align-items-center gap-3 mb-3">
        <button class="btn btn-link text-secondary p-0" @click="$router.back()">
          <IconFa name="arrow-left" size="1.5rem" />
        </button>
        <h4 class="mb-0 fw-bold">Обращение #{{ problem?.public_id?.substring(0, 8) }}</h4>
      </div>
    </template>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-civic"></div>
    </div>

    <div v-else-if="problem" class="problem-details">
      <!-- Status and priority -->
      <div class="d-flex gap-2 mb-3">
        <ProblemStatusBadge :status="problem.status" />
        <UiBadge v-if="problem.priority_id === 1" variant="danger">Критическая</UiBadge>
      </div>

      <!-- Title and description -->
      <h5 class="fw-bold mb-2">{{ problem.title }}</h5>
      <p class="text-muted mb-4">{{ problem.description || 'Описание не указано' }}</p>

      <!-- Meta info -->
      <div class="card bg-light border-0 mb-4">
        <div class="card-body p-3">
          <div class="row g-3">
            <div class="col-6 col-md-3">
              <small class="text-muted d-block">Создано</small>
              <strong>{{ formatDate(problem.created_at) }}</strong>
            </div>
            <div class="col-6 col-md-3">
              <small class="text-muted d-block">Подтверждений</small>
              <strong>{{ problem.confirmations_count || 0 }}</strong>
            </div>
            <div class="col-6 col-md-3">
              <small class="text-muted d-block">Рейтинг</small>
              <strong>{{ problem.rating?.toFixed(1) || '0.0' }}</strong>
            </div>
            <div class="col-6 col-md-3">
              <small class="text-muted d-block">Автор</small>
              <strong>{{ problem.created_by?.full_name || 'Неизвестно' }}</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Attachments -->
      <ProblemAttachments :attachments="problem.attachments || []" />

      <!-- Timeline -->
      <div class="mt-4">
        <h6 class="fw-bold mb-3">
          <IconFa name="clock-history" class="me-2" /> История изменений
        </h6>
        <ProblemTimeline :history="problem.status_history || []" />
      </div>

      <!-- Actions -->
      <div class="d-flex gap-2 mt-4">
        <UiButton variant="primary" @click="openChat">
          <IconFa name="chat-dots" class="me-2" /> Открыть чат
        </UiButton>
        <UiButton variant="outline-secondary" @click="downloadDocx">
          <IconFa name="download" class="me-2" /> Скачать DOCX
        </UiButton>
        <UiButton v-if="canConfirm" variant="success" @click="confirmProblem">
          <IconFa name="check2" class="me-2" /> Подтвердить
        </UiButton>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <IconFa name="exclamation-triangle" size="3rem" color="#adb5bd" />
      <p class="text-muted mt-3">Проблема не найдена</p>
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import UiButton from '@/components/ui/UiButton.vue'
import ProblemStatusBadge from '@/components/problems/ProblemStatusBadge.vue'
import ProblemAttachments from '@/components/problems/ProblemAttachments.vue'
import ProblemTimeline from '@/components/problems/ProblemTimeline.vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'ProblemDetailsView',
  components: {
    AppPageContainer, IconFa, UiBadge, UiButton,
    ProblemStatusBadge, ProblemAttachments, ProblemTimeline
  },
  props: {
    id: { type: [String, Number], required: true }
  },
  data() {
    return {
      problem: null,
      isLoading: false
    }
  },
  computed: {
    problemsStore() {
      return useProblemsStore()
    },
    canConfirm() {
      const { isAuthenticated } = useAuth()
      return isAuthenticated && !['resolved', 'closed'].includes(this.problem?.status)
    }
  },
  async mounted() {
    await this.loadProblem()
  },
  methods: {
    async loadProblem() {
      this.isLoading = true
      try {
        this.problem = await this.problemsStore.fetchProblem(this.id)
      } catch (error) {
        console.error('Failed to load problem:', error)
      } finally {
        this.isLoading = false
      }
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      })
    },

    openChat() {
      this.$router.push({ name: 'ProblemChat', params: { id: this.id } })
    },

    downloadDocx() {
      // TODO: Реализовать скачивание DOCX
      alert('Скачивание DOCX будет реализовано позже')
    },

    async confirmProblem() {
      try {
        await this.problemsStore.confirmProblem(this.id)
        await this.loadProblem()
        alert('Проблема подтверждена')
      } catch (error) {
        console.error('Failed to confirm problem:', error)
      }
    }
  }
}
</script>

<style scoped>
.problem-details {
  max-width: 800px;
}
</style>