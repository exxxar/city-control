<!-- client/src/views/executor/AssignedProblemsView.vue -->
<template>
  <AppPageContainer title="Назначенные проблемы">
    <!-- Filters -->
    <div class="card shadow-sm mb-3">
      <div class="card-body p-3">
        <div class="row g-2">
          <div class="col-12 col-md-4">
            <UiSelect v-model="filters.status" placeholder="Все статусы">
              <option value="">Все статусы</option>
              <option value="new">Новые</option>
              <option value="in_progress">В работе</option>
              <option value="solution_ready">Решение готово</option>
            </UiSelect>
          </div>
          <div class="col-12 col-md-4">
            <UiSelect v-model="filters.priority" placeholder="Все приоритеты">
              <option value="">Все приоритеты</option>
              <option value="1">Критический</option>
              <option value="2">Высокий</option>
              <option value="3">Средний</option>
              <option value="4">Низкий</option>
            </UiSelect>
          </div>
          <div class="col-12 col-md-4">
            <UiSelect v-model="filters.sla" placeholder="SLA статус">
              <option value="">Все</option>
              <option value="overdue">Просрочено</option>
              <option value="urgent">Срочно</option>
              <option value="normal">В норме</option>
            </UiSelect>
          </div>
        </div>
      </div>
    </div>

    <!-- Problems list -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-civic"></div>
    </div>

    <div v-else-if="problems.length === 0" class="py-5">
      <UiEmptyState
        icon="check-circle"
        title="Нет назначенных проблем"
        description="Все задачи выполнены или вам ещё не назначены проблемы"
      />
    </div>

    <div v-else>
      <ProblemCard
        v-for="problem in problems"
        :key="problem.id"
        :problem="problem"
        @click="openProblem"
      />

      <UiPagination
        v-if="pagination.pages > 1"
        :current-page="pagination.page"
        :total-pages="pagination.pages"
        @update:current-page="changePage"
      />
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import UiSelect from '@/components/ui/UiSelect.vue'
import UiEmptyState from '@/components/ui/UiEmptyState.vue'
import UiPagination from '@/components/ui/UiPagination.vue'
import ProblemCard from '@/components/problems/ProblemCard.vue'
import * as problemsApi from '@/api/problems.api'

export default {
  name: 'AssignedProblemsView',
  components: { AppPageContainer, UiSelect, UiEmptyState, UiPagination, ProblemCard },
  data() {
    return {
      filters: {
        status: '',
        priority: '',
        sla: ''
      },
      problems: [],
      pagination: { page: 1, per_page: 20, pages: 0, total: 0 },
      isLoading: false
    }
  },
  watch: {
    filters: {
      handler() {
        this.pagination.page = 1
        this.loadProblems()
      },
      deep: true
    }
  },
  async mounted() {
    await this.loadProblems()
  },
  methods: {
    async loadProblems() {
      this.isLoading = true
      try {
        const response = await problemsApi.getProblems({
          assigned_to_me: true,
          ...this.filters,
          page: this.pagination.page,
          per_page: this.pagination.per_page
        })

        this.problems = response.items || response
        if (response.total !== undefined) {
          this.pagination = {
            page: response.page,
            per_page: response.per_page,
            pages: response.pages,
            total: response.total
          }
        }
      } catch (error) {
        console.error('Failed to load problems:', error)
      } finally {
        this.isLoading = false
      }
    },

    changePage(page) {
      this.pagination.page = page
      this.loadProblems()
    },

    openProblem(problem) {
      this.$router.push({ name: 'ProblemDetails', params: { id: problem.id } })
    }
  }
}
</script>