<!-- client/src/views/problems/MyProblemsView.vue -->
<template>
  <AppPageContainer>
    <!-- Современный заголовок с действиями -->
    <template #header>
      <div class="page-header-modern">
        <div>
          <h2 class="page-title">Мои обращения</h2>
          <p class="page-subtitle">Управляйте своими заявками и отслеживайте статус</p>
        </div>
        <router-link to="/create" class="btn-create-modern">
          <IconFa name="plus" class="me-2" />
          <span class="d-none d-sm-inline">Новое обращение</span>
          <span class="d-sm-none">Создать</span>
        </router-link>
      </div>
    </template>

    <!-- Фильтры (с кнопкой сворачивания на мобильных) -->
    <div class="filters-container mb-4">
      <div class="d-flex justify-content-between align-items-center mb-2 d-md-none">
        <span class="fw-bold small text-muted">
          <IconFa name="filter" class="me-1" /> Фильтры
        </span>
        <button class="btn btn-sm btn-link text-civic p-0" @click="showFilters = !showFilters">
          {{ showFilters ? 'Скрыть' : 'Показать' }}
        </button>
      </div>

      <Transition name="slide-down">
        <div v-show="showFilters" class="filters-card">
          <ProblemFilters
              :categories="categories"
              :priorities="priorities"
              :initial-filters="filters"
              @apply="applyFilters"
              @reset="resetFilters"
          />
        </div>
      </Transition>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-modern">
        <div class="spinner-border text-civic" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
      </div>
      <p class="text-muted small mt-3">Загружаем ваши обращения...</p>
    </div>

    <!-- Пустое состояние и список (с анимацией переключения) -->
    <Transition v-else name="fade" mode="out-in">
      <div v-if="problems.length === 0" class="empty-state" key="empty">
        <div class="empty-icon-wrapper">
          <IconFa name="inbox" size="3rem" color="#cbd5e1" />
        </div>
        <h4 class="fw-bold mt-3">Список обращений пуст</h4>
        <p class="text-muted mb-4">Вы еще не создали ни одного обращения. Самое время исправить это!</p>
        <router-link to="/create" class="btn-civic-modern">
          <IconFa name="plus-circle" class="me-2" />
          Создать первое обращение
        </router-link>
      </div>

      <!-- Список проблем -->
      <div v-else key="list" class="problems-list">
        <TransitionGroup name="list" tag="div" class="d-flex flex-column gap-3">
          <ProblemCard
              v-for="problem in problems"
              :key="problem.id"
              :problem="problem"
              @click="openProblem"
          />
        </TransitionGroup>

        <!-- Пагинация -->
        <div v-if="pagination.pages > 1" class="pagination-wrapper mt-4">
          <UiPagination
              :current-page="pagination.page"
              :total-pages="pagination.pages"
              @update:current-page="changePage"
          />
        </div>
      </div>
    </Transition>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import UiPagination from '@/components/ui/UiPagination.vue'
import ProblemCard from '@/components/problems/ProblemCard.vue'
import ProblemFilters from '@/components/problems/ProblemFilters.vue'
import { useProblemsStore } from '@/stores/problems.store'
import * as categoriesApi from '@/api/categories.api'

export default {
  name: 'MyProblemsView',
  components: {
    AppPageContainer,
    IconFa,
    UiPagination,
    ProblemCard,
    ProblemFilters
  },
  data() {
    return {
      problems: [],
      categories: [],
      priorities: [
        { id: 1, name: 'Критический' },
        { id: 2, name: 'Высокий' },
        { id: 3, name: 'Средний' },
        { id: 4, name: 'Низкий' }
      ],
      filters: {},
      pagination: { page: 1, per_page: 10, pages: 0, total: 0 },
      isLoading: false,
      showFilters: true // По умолчанию открыты на десктопе, управляется на мобильном
    }
  },
  computed: {
    problemsStore() {
      return useProblemsStore()
    }
  },
  async mounted() {
    // На мобильных устройствах фильтры по умолчанию скрыты для экономии места
    if (window.innerWidth < 768) {
      this.showFilters = false
    }
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        await Promise.all([
          this.loadProblems(),
          this.loadCategories()
        ])
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        this.isLoading = false
      }
    },

    async loadProblems() {
      const response = await this.problemsStore.fetchMyProblems({
        page: this.pagination.page,
        per_page: this.pagination.per_page,
        ...this.filters
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
    },

    async loadCategories() {
      try {
        this.categories = await categoriesApi.getCategories()
      } catch (error) {
        console.error('Failed to load categories:', error)
      }
    },

    applyFilters(newFilters) {
      this.filters = newFilters
      this.pagination.page = 1
      this.loadProblems()
      // На мобильном закрываем фильтры после применения
      if (window.innerWidth < 768) {
        this.showFilters = false
      }
    },

    resetFilters() {
      this.filters = {}
      this.pagination.page = 1
      this.loadProblems()
    },

    changePage(page) {
      this.pagination.page = page
      this.loadProblems()
      // Прокрутка наверх при смене страницы
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    openProblem(problem) {
      this.$router.push({ name: 'ProblemDetails', params: { id: problem.id } })
    }
  }
}
</script>

<style scoped>
/* === Заголовок страницы === */
.page-header-modern {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0;
}

.page-subtitle {
  color: #70808c;
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

.btn-create-modern {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-weight: 700;
  border-radius: 14px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
  transition: all 0.2s ease;
}

.btn-create-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
  color: white;
}

/* === Фильтры === */
.filters-card {
  background: #ffffff;
  border: 1px solid #e8edf0;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 4px 12px rgba(23, 47, 64, 0.03);
}

/* === Состояние загрузки === */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
}

.spinner-modern .spinner-border {
  width: 2.5rem;
  height: 2.5rem;
  color: #00a896 !important;
}

/* === Пустое состояние === */
.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  background: #ffffff;
  border-radius: 20px;
  border: 1px dashed #e8edf0;
}

.empty-icon-wrapper {
  display: inline-flex;
  width: 80px;
  height: 80px;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 50%;
}

.btn-civic-modern {
  display: inline-flex;
  align-items: center;
  padding: 0.85rem 1.75rem;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-weight: 700;
  border-radius: 14px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
  transition: all 0.2s ease;
}

.btn-civic-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
  color: white;
}

/* === Анимации === */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}
.slide-down-enter-to,
.slide-down-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px; /* Достаточно для контента фильтров */
}

/* Анимация появления списка */
.list-enter-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

/* === Пагинация === */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 1rem;
}

/* === Мобильная адаптация === */
@media (max-width: 767.98px) {
  .page-header-modern {
    align-items: stretch;
    flex-direction: column;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .btn-create-modern {
    justify-content: center;
    width: 100%;
  }

  .filters-card {
    padding: 1rem;
  }
}
</style>