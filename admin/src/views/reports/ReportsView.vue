<!-- admin/src/views/reports/ReportsView.vue -->
<template>
  <div class="reports-page">
    <!-- Заголовок -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Отчёты исполнителей</h1>
        <p class="page-subtitle">Проверка выполненных работ по обращениям граждан</p>

        <button class="btn-export" @click="handleExport">
          <i class="fas fa-file-excel"></i>
          Экспорт в Excel
        </button>
      </div>
      <div class="page-stats">
        <div class="stat-badge stat-badge--warning">
          <i class="fas fa-clock"></i>
          <span>На проверке: {{ reportsStore.pendingCount }}</span>
        </div>
        <div class="stat-badge stat-badge--info">
          <i class="fas fa-redo"></i>
          <span>На доработке: {{ reportsStore.revisionCount }}</span>
        </div>
      </div>
    </div>

    <!-- Уведомление о моковых данных -->
    <Transition name="fade">
      <div v-if="reportsStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные. API отчётов на бэкенде пока не настроен.</span>
      </div>
    </Transition>

    <!-- Фильтры -->
    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Поиск</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-search"></i></span>
            <input v-model="filters.search" type="text" class="form-control-custom" placeholder="Проблема или исполнитель" @input="debouncedSearch">
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Статус</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-filter"></i></span>
            <select v-model="filters.status" class="form-control-custom" @change="applyFilters">
              <option value="">Все статусы</option>
              <option value="pending">⏳ На проверке</option>
              <option value="approved">✅ Приняты</option>
              <option value="rejected">❌ Отклонены</option>
              <option value="revision">🔄 На доработке</option>
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
      <div v-if="reportsStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка отчётов...</p>
      </div>

      <div v-else-if="reportsStore.reports.length === 0" class="empty-state">
        <i class="fas fa-file-circle-xmark"></i>
        <h3>Отчёты не найдены</h3>
      </div>

      <div v-else class="table-wrapper">
        <table class="reports-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>Проблема</th>
            <th>Исполнитель</th>
            <th>Дата выполнения</th>
            <th>Статус</th>
            <th>Отправлен</th>
            <th class="actions-column">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="report in reportsStore.reports" :key="report.id">
            <td class="col-id">#{{ report.id }}</td>
            <td>
              <div class="problem-cell">
                <div class="problem-title">{{ report.problem_title }}</div>
                <div class="problem-id">Обращение #{{ report.problem_id }}</div>
              </div>
            </td>
            <td>
              <div class="executor-cell">
                <i class="fas fa-user-tie"></i>
                <span>{{ report.executor_name }}</span>
              </div>
            </td>
            <td class="col-date">{{ formatDate(report.work_date) }}</td>
            <td>
                <span class="status-badge" :class="`status-${report.status}`">
                  {{ getStatusLabel(report.status) }}
                </span>
            </td>
            <td class="col-date">{{ formatDateTime(report.submitted_at) }}</td>
            <td>
              <button class="action-btn action-btn--primary" @click="openDetailModal(report)" title="Просмотр отчёта">
                <i class="fas fa-eye"></i>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <div v-if="reportsStore.pagination.pages > 1" class="pagination">
        <button class="pagination-btn" :disabled="reportsStore.pagination.page === 1" @click="goToPage(reportsStore.pagination.page - 1)">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="pagination-info">Стр. {{ reportsStore.pagination.page }} из {{ reportsStore.pagination.pages }}</span>
        <button class="pagination-btn" :disabled="reportsStore.pagination.page === reportsStore.pagination.pages" @click="goToPage(reportsStore.pagination.page + 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Модальное окно деталей отчёта -->
    <ReportDetailModal
        v-if="selectedReport"
        :report="selectedReport"
        @close="selectedReport = null"
        @approved="onReportApproved"
        @rejected="onReportRejected"
        @revision="onReportRevision"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useReportsStore } from '@/stores/reports.store'
import { useNotifications } from '@/composables/useNotifications'
import ReportDetailModal from '@/components/reports/ReportDetailModal.vue'

import { useExport } from '@/composables/useExport'

const { exportToExcel } = useExport()

// В admin/src/views/reports/ReportsView.vue

function handleExport() {
  const exportData = reportsStore.reports.map(r => ({
    'ID': r.id,
    'Проблема': r.problem_title || (r.problem ? r.problem.title : 'Не указано'),
    'Исполнитель': r.executor_name || (r.executor ? r.executor.full_name : 'Не указано'),
    'Дата выполнения': formatDate(r.work_date),
    'Статус': getStatusLabel(r.status),
    'Стоимость (₽)': r.cost ? `${r.cost.toLocaleString('ru-RU')} ₽` : '0 ₽'
  }))

  exportToExcel(exportData, 'отчёты_исполнителей', 'Отчёты')
}

const reportsStore = useReportsStore()
const { success, error: showError } = useNotifications()

const filters = reactive({ search: '', status: '' })
const selectedReport = ref(null)
let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(applyFilters, 300)
}

function applyFilters() {
  reportsStore.pagination.page = 1
  loadReports()
}

function resetFilters() {
  filters.search = ''
  filters.status = ''
  applyFilters()
}

function goToPage(page) {
  reportsStore.pagination.page = page
  loadReports()
}

async function loadReports() {
  const params = {
    page: reportsStore.pagination.page,
    per_page: reportsStore.pagination.per_page
  }
  if (filters.search) params.search = filters.search
  if (filters.status) params.status = filters.status

  await reportsStore.fetchReports(params)
}

function getStatusLabel(status) {
  const labels = {
    pending: 'На проверке',
    approved: 'Принят',
    rejected: 'Отклонён',
    revision: 'На доработке'
  }
  return labels[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

function formatDateTime(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

function openDetailModal(report) {
  selectedReport.value = { ...report }
}

async function onReportApproved() {
  selectedReport.value = null
  await loadReports()
  success('Отчёт принят, проблема закрыта')
}

async function onReportRejected() {
  selectedReport.value = null
  await loadReports()
  success('Отчёт отклонён')
}

async function onReportRevision() {
  selectedReport.value = null
  await loadReports()
  success('Отчёт возвращён на доработку')
}

onMounted(() => {
  loadReports()
})
</script>

<style scoped lang="scss">
.reports-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }
.page-stats { display: flex; gap: 0.75rem; }

.stat-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.85rem; font-weight: 700; }
.stat-badge--warning { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.stat-badge--info { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }

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
.reports-table { width: 100%; border-collapse: collapse; }
.reports-table th, .reports-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.reports-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.reports-table tbody tr:hover { background: #f8fafc; }
.col-id { font-weight: 700; color: #70808c; font-size: 0.85rem; }

.problem-cell .problem-title { font-weight: 700; color: #172f40; font-size: 0.92rem; margin-bottom: 0.25rem; }
.problem-cell .problem-id { color: #70808c; font-size: 0.78rem; }

.executor-cell { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: #172f40; font-weight: 600; }
.executor-cell i { color: #00a896; }

.col-date { color: #70808c; font-size: 0.85rem; white-space: nowrap; }

.status-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; }
.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.status-revision { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }

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
  .reports-table th:nth-child(4), .reports-table td:nth-child(4),
  .reports-table th:nth-child(6), .reports-table td:nth-child(6) { display: none; }
}

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

</style>