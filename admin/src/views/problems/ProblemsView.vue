<!-- admin/src/views/problems/ProblemsView.vue -->
<template>
  <div class="problems-page">
    <!-- Заголовок -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">Обращения граждан</h1>
        <p class="page-subtitle">Модерация и назначение исполнителей</p>
      </div>
      <div class="header-right">
        <button class="btn-export" @click="handleExport">
          <i class="fas fa-file-excel"></i>
          <span>Экспорт в Excel</span>
        </button>
      </div>
    </div>

    <!-- Уведомление о моковых данных -->
    <Transition name="fade">
      <div v-if="problemsStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные. Проверьте подключение к API бэкенда.</span>
      </div>
    </Transition>

    <!-- Фильтры -->
    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Поиск</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-search"></i></span>
            <input v-model="filters.search" type="text" class="form-control-custom" placeholder="Описание, адрес или автор" @input="debouncedSearch">
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Статус</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-filter"></i></span>
            <select v-model="filters.status" class="form-control-custom" @change="applyFilters">
              <option value="">Все статусы</option>
              <option value="new">🔴 Новые</option>
              <option value="approved">🟢 Одобрены</option>
              <option value="in_progress">🟠 В работе</option>
              <option value="resolved">✅ Решены</option>
              <option value="rejected">⚫ Отклонены</option>
            </select>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">&nbsp;</label>
          <button class="btn-reset" @click="resetFilters">
            <i class="fas fa-rotate-left"></i> Сбросить
          </button>
        </div>
      </div>
    </div>

    <!-- Таблица -->
    <div class="table-card">
      <div v-if="problemsStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка обращений...</p>
      </div>

      <div v-else-if="problemsStore.problems.length === 0" class="empty-state">
        <i class="fas fa-inbox"></i>
        <h3>Обращения не найдены</h3>
      </div>

      <div v-else class="table-wrapper">
        <table class="problems-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>Проблема</th>
            <th>Категория</th>
            <th>Автор</th>
            <th>Статус</th>
            <th>Дата</th>
            <th class="actions-column">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="problem in problemsStore.problems" :key="problem.id">
            <td class="col-id">#{{ problem.id }}</td>
            <td>
              <div class="problem-title-cell">
                <div class="title">{{ problem.title }}</div>
                <div class="address"><i class="fas fa-location-dot"></i> {{ problem.address }}</div>
              </div>
            </td>
            <td>
                <span class="category-badge">
                  {{ typeof problem.category === 'object' ? problem.category?.name : problem.category }}
                </span>
            </td>
            <td>
              <div class="author-cell">
                <div>{{ typeof problem.author === 'object' ? problem.author?.full_name : problem.author }}</div>
                <div class="phone">{{ typeof problem.author === 'object' ? problem.author?.phone : problem.phone }}</div>
              </div>
            </td>
            <td>
                <span class="status-badge" :class="`status-${problem.status}`">
                  {{ getStatusLabel(problem.status) }}
                </span>
            </td>
            <td class="col-date">{{ formatDate(problem.created_at) }}</td>
            <td>
              <button class="action-btn action-btn--primary" @click="openDetailModal(problem)" title="Подробнее / Модерация">
                <i class="fas fa-eye"></i>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <div v-if="problemsStore.pagination.pages > 1" class="pagination">
        <button class="pagination-btn" :disabled="problemsStore.pagination.page === 1" @click="goToPage(problemsStore.pagination.page - 1)">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="pagination-info">Стр. {{ problemsStore.pagination.page }} из {{ problemsStore.pagination.pages }}</span>
        <button class="pagination-btn" :disabled="problemsStore.pagination.page === problemsStore.pagination.pages" @click="goToPage(problemsStore.pagination.page + 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Модальное окно деталей и модерации -->
    <ProblemDetailModal
        v-if="selectedProblem"
        :problem="selectedProblem"
        :executors="problemsStore.executors"
        @close="selectedProblem = null"
        @moderated="onProblemModerated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useNotifications } from '@/composables/useNotifications'
import ProblemDetailModal from '@/components/problems/ProblemDetailModal.vue'
import { useExport } from '@/composables/useExport'

const problemsStore = useProblemsStore()
const { success, error: showError } = useNotifications()
const { exportToExcel } = useExport()

const filters = reactive({ search: '', status: '' })
const selectedProblem = ref(null)
let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(applyFilters, 300)
}

function applyFilters() {
  problemsStore.pagination.page = 1
  loadProblems()
}

function resetFilters() {
  filters.search = ''
  filters.status = ''
  applyFilters()
}

function goToPage(page) {
  problemsStore.pagination.page = page
  loadProblems()
}

async function loadProblems() {
  const params = {
    page: problemsStore.pagination.page,
    per_page: problemsStore.pagination.per_page
  }
  if (filters.search) params.search = filters.search
  if (filters.status) params.status = filters.status

  await problemsStore.fetchProblems(params)
}

function getStatusLabel(status) {
  const labels = {
    new: 'Новое',
    approved: 'Одобрено',
    in_progress: 'В работе',
    resolved: 'Решено',
    rejected: 'Отклонено'
  }
  return labels[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

function openDetailModal(problem) {
  selectedProblem.value = { ...problem }
}

async function onProblemModerated() {
  selectedProblem.value = null
  await loadProblems()
  success('Статус обращения обновлен')
}

function handleExport() {
  // Безопасный маппинг для реальных данных (где author/category могут быть объектами)
  const exportData = problemsStore.problems.map(p => ({
    'ID': p.id,
    'Проблема': p.title,
    'Категория': typeof p.category === 'object' ? p.category?.name : p.category,
    'Адрес': p.address,
    'Автор': typeof p.author === 'object' ? p.author?.full_name : p.author,
    'Телефон': typeof p.author === 'object' ? p.author?.phone : p.phone,
    'Статус': getStatusLabel(p.status),
    'Дата создания': formatDate(p.created_at)
  }))

  exportToExcel(exportData, 'обращения_граждан', 'Обращения')
}

onMounted(async () => {
  await problemsStore.fetchExecutors()
  await loadProblems()
})
</script>

<style scoped lang="scss">
.problems-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}
.header-left { flex: 1; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

/* Стильная кнопка Excel */
.btn-export {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1.35rem;
  background: linear-gradient(135deg, #217346, #185c37);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 12px rgba(33, 115, 70, 0.25);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(33, 115, 70, 0.35);
  }

  i {
    font-size: 1.15rem;
    color: #a3e635; /* Светло-зеленый акцент для иконки */
  }
}

.page-stats { display: flex; gap: 0.75rem; }
.stat-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.85rem; font-weight: 700; }
.stat-badge--danger { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.stat-badge--warning { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.filters-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; }
.filters-grid { display: grid; grid-template-columns: 2fr 1fr auto; gap: 1rem; }
.filter-group { display: flex; flex-direction: column; }
.filter-label { display: block; margin-bottom: 0.45rem; color: #172f40; font-size: 0.82rem; font-weight: 700; }
.input-wrapper { display: flex; align-items: center; border: 1px solid #e8edf0; border-radius: 12px; background: #fcfcfd; transition: all 180ms ease; overflow: hidden; }
.input-wrapper:focus-within { border-color: #00a896; background: white; box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1); }
.input-icon { display: flex; align-items: center; justify-content: center; width: 42px; flex-shrink: 0; color: #70808c; }
.form-control-custom { flex: 1; border: none; background: transparent; padding: 0.75rem 1rem 0.75rem 0; color: #172f40; font-size: 0.9rem; width: 100%; outline: none; }
.btn-reset { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; background: #f1f5f9; border: 1px solid #e8edf0; border-radius: 12px; color: #172f40; font-size: 0.88rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; }
.btn-reset:hover { background: #e2e8f0; }

.table-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; overflow: hidden; }
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; color: #70808c; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state i { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; }

.table-wrapper { overflow-x: auto; }
.problems-table { width: 100%; border-collapse: collapse; }
.problems-table th, .problems-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.problems-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.problems-table tbody tr:hover { background: #f8fafc; }
.col-id { font-weight: 700; color: #70808c; font-size: 0.85rem; }
.problem-title-cell .title { font-weight: 700; color: #172f40; font-size: 0.92rem; margin-bottom: 0.25rem; }
.problem-title-cell .address { color: #70808c; font-size: 0.82rem; display: flex; align-items: center; gap: 0.35rem; }
.category-badge { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 8px; background: rgba(13, 202, 240, 0.12); color: #0dcaf0; font-size: 0.78rem; font-weight: 700; }
.author-cell { font-size: 0.9rem; color: #172f40; font-weight: 600; }
.author-cell .phone { font-size: 0.78rem; color: #70808c; font-weight: 400; margin-top: 0.15rem; }

.status-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; }
.status-new { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-in_progress { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-resolved { background: rgba(0, 168, 150, 0.12); color: #00a896; }
.status-rejected { background: rgba(113, 128, 150, 0.12); color: #70808c; }

.col-date { color: #70808c; font-size: 0.85rem; white-space: nowrap; }
.actions-column { width: 80px; }
.action-btn { width: 36px; height: 36px; border-radius: 10px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; transition: all 0.2s ease; }
.action-btn--primary { background: rgba(0, 168, 150, 0.12); color: #00a896; }
.action-btn--primary:hover { background: #00a896; color: white; }

.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; padding: 1.25rem; border-top: 1px solid #e8edf0; }
.pagination-btn { width: 36px; height: 36px; border-radius: 10px; border: 1px solid #e8edf0; background: white; color: #172f40; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.pagination-btn:hover:not(:disabled) { background: #f8fafc; border-color: #00a896; color: #00a896; }
.pagination-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination-info { color: #70808c; font-size: 0.88rem; font-weight: 600; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 991.98px) {
  .filters-grid { grid-template-columns: 1fr; }
  .problems-table th:nth-child(3), .problems-table td:nth-child(3),
  .problems-table th:nth-child(4), .problems-table td:nth-child(4) { display: none; }
  .page-header { flex-direction: column; }
  .btn-export { width: 100%; justify-content: center; }
}
</style>