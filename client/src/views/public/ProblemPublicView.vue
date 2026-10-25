<!-- client/src/views/public/ProblemPublicView.vue -->
<template>

    <div class="container py-4">
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-civic"></div>
      </div>

      <div v-else-if="problem" class="problem-public-view">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-start mb-4">
          <div>
            <ProblemStatusBadge :status="problem.status" />
            <h3 class="mt-2 mb-1 fw-bold">{{ problem.title }}</h3>
            <p class="text-muted mb-0">{{ formatDate(problem.created_at) }}</p>
          </div>
          <router-link to="/login" class="btn btn-civic">
            <IconFa name="box-arrow-in-right" class="me-2" /> Войти, чтобы участвовать
          </router-link>
        </div>

        <!-- Description -->
        <div class="card mb-4">
          <div class="card-body">
            <h6 class="fw-bold mb-2">Описание</h6>
            <p class="mb-0">{{ problem.description || 'Описание не указано' }}</p>
          </div>
        </div>

        <!-- Attachments -->
        <ProblemAttachments :attachments="problem.attachments || []" />

        <!-- Stats -->
        <div class="row g-3 mt-4">
          <div class="col-6 col-md-3">
            <div class="card text-center">
              <div class="card-body">
                <IconFa name="people" size="1.5rem" color="var(--civic-primary)" />
                <div class="h4 mb-0 mt-2">{{ problem.confirmations_count || 0 }}</div>
                <small class="text-muted">Подтверждений</small>
              </div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card text-center">
              <div class="card-body">
                <IconFa name="chat-dots" size="1.5rem" color="var(--civic-primary)" />
                <div class="h4 mb-0 mt-2">{{ problem.messages_count || 0 }}</div>
                <small class="text-muted">Сообщений</small>
              </div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card text-center">
              <div class="card-body">
                <IconFa name="star-fill" size="1.5rem" color="#FFD166" />
                <div class="h4 mb-0 mt-2">{{ problem.rating?.toFixed(1) || '0.0' }}</div>
                <small class="text-muted">Рейтинг</small>
              </div>
            </div>
          </div>
          <div class="col-6 col-md-3">
            <div class="card text-center">
              <div class="card-body">
                <IconFa name="clock-history" size="1.5rem" color="var(--civic-primary)" />
                <div class="h4 mb-0 mt-2">{{ problem.status_history?.length || 0 }}</div>
                <small class="text-muted">Изменений</small>
              </div>
            </div>
          </div>
        </div>

        <!-- CTA -->
        <div class="text-center mt-5">
          <h5 class="fw-bold mb-3">Хотите помочь решить эту проблему?</h5>
          <router-link to="/register" class="btn btn-civic btn-lg">
            Зарегистрироваться и участвовать
          </router-link>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <IconFa name="exclamation-triangle" size="3rem" color="#adb5bd" />
        <p class="text-muted mt-3">Проблема не найдена</p>
      </div>
    </div>

</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'
import ProblemStatusBadge from '@/components/problems/ProblemStatusBadge.vue'
import ProblemAttachments from '@/components/problems/ProblemAttachments.vue'
import * as problemsApi from '@/api/problems.api'

export default {
  name: 'ProblemPublicView',
  components: { PublicLayout, IconFa, ProblemStatusBadge, ProblemAttachments },
  props: {
    id: { type: [String, Number], required: true }
  },
  data() {
    return {
      problem: null,
      isLoading: false
    }
  },
  async mounted() {
    await this.loadProblem()
  },
  methods: {
    async loadProblem() {
      this.isLoading = true
      try {
        this.problem = await problemsApi.getProblem(this.id)
      } catch (error) {
        console.error('Failed to load problem:', error)
      } finally {
        this.isLoading = false
      }
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      })
    }
  }
}
</script>