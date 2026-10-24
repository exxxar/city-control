<!-- client/src/views/executor/ExecutorDashboardView.vue -->
<template>
  <AppPageContainer title="Панель исполнителя">
    <!-- Statistics cards -->
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="small opacity-75">Новые</div>
                <div class="h3 mb-0">{{ stats.new_count }}</div>
              </div>
              <IconFa name="inbox" size="2rem" />
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card bg-warning text-dark">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="small opacity-75">В работе</div>
                <div class="h3 mb-0">{{ stats.in_progress_count }}</div>
              </div>
              <IconFa name="gear" size="2rem" />
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card bg-danger text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="small opacity-75">Просрочено</div>
                <div class="h3 mb-0">{{ stats.overdue_count }}</div>
              </div>
              <IconFa name="exclamation-triangle" size="2rem" />
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="small opacity-75">Решено сегодня</div>
                <div class="h3 mb-0">{{ stats.resolved_today }}</div>
              </div>
              <IconFa name="check-circle" size="2rem" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Assigned problems -->
    <div class="card">
      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <h6 class="mb-0 fw-bold">Назначенные проблемы</h6>
        <router-link to="/executor/problems" class="btn btn-sm btn-outline-primary">
          Все задачи
        </router-link>
      </div>
      <div class="card-body p-0">
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border text-civic"></div>
        </div>

        <div v-else-if="assignedProblems.length === 0" class="text-center py-5">
          <IconFa name="check-circle" size="3rem" color="#06D6A0" />
          <p class="text-muted mt-3">Нет назначенных проблем</p>
        </div>

        <div v-else class="list-group list-group-flush">
          <div
            v-for="problem in assignedProblems.slice(0, 5)"
            :key="problem.id"
            class="list-group-item list-group-item-action"
            @click="openProblem(problem)"
          >
            <div class="d-flex justify-content-between align-items-start">
              <div class="flex-grow-1">
                <div class="d-flex gap-2 mb-1">
                  <ProblemStatusBadge :status="problem.status" size="sm" />
                  <UiBadge v-if="isOverdue(problem)" variant="danger" size="sm">Просрочено</UiBadge>
                </div>
                <h6 class="mb-1">{{ problem.title }}</h6>
                <small class="text-muted">{{ formatDate(problem.created_at) }}</small>
              </div>
              <IconFa name="chevron-right" color="#adb5bd" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import ProblemStatusBadge from '@/components/problems/ProblemStatusBadge.vue'
import * as problemsApi from '@/api/problems.api'

export default {
  name: 'ExecutorDashboardView',
  components: { AppPageContainer, IconFa, UiBadge, ProblemStatusBadge },
  data() {
    return {
      stats: {
        new_count: 0,
        in_progress_count: 0,
        overdue_count: 0,
        resolved_today: 0
      },
      assignedProblems: [],
      isLoading: false
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        // Загружаем статистику и назначенные проблемы
        const [statsResponse, problemsResponse] = await Promise.all([
          this.loadStats(),
          this.loadAssignedProblems()
        ])
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        this.isLoading = false
      }
    },

    async loadStats() {
      // TODO: Реализовать API для статистики исполнителя
      // Пока используем мок-данные
      this.stats = {
        new_count: 5,
        in_progress_count: 12,
        overdue_count: 2,
        resolved_today: 3
      }
    },

    async loadAssignedProblems() {
      try {
        const response = await problemsApi.getProblems({
          assigned_to_me: true,
          status: ['new', 'in_progress', 'accepted']
        })
        this.assignedProblems = response.items || response
      } catch (error) {
        console.error('Failed to load assigned problems:', error)
      }
    },

    isOverdue(problem) {
      // TODO: Проверять SLA таймеры
      return false
    },

    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },

    openProblem(problem) {
      this.$router.push({ name: 'ProblemDetails', params: { id: problem.id } })
    }
  }
}
</script>