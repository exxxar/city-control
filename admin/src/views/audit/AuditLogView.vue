<!-- admin/src/views/audit/AuditLogView.vue -->
<template>
  <div class="audit-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Журнал действий</h1>
        <p class="page-subtitle">История всех действий администраторов и модераторов</p>
      </div>
    </div>

    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Пользователь</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-user"></i></span>
            <input v-model="filters.user" type="text" class="form-control-custom" placeholder="Имя пользователя" @input="debouncedSearch">
          </div>
        </div>
        <div class="filter-group">
          <label class="filter-label">Действие</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-filter"></i></span>
            <select v-model="filters.action" class="form-control-custom" @change="loadLogs">
              <option value="">Все действия</option>
              <option value="user_blocked">Блокировка пользователя</option>
              <option value="problem_approved">Одобрение обращения</option>
              <option value="report_rejected">Отклонение отчёта</option>
              <option value="category_created">Создание категории</option>
              <option value="settings_updated">Изменение настроек</option>
            </select>
          </div>
        </div>
        <div class="filter-group">
          <label class="filter-label">&nbsp;</label>
          <button class="btn-reset" @click="resetFilters"><i class="fas fa-rotate-left"></i> Сбросить</button>
        </div>
      </div>
    </div>

    <div class="table-card">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка журнала...</p>
      </div>

      <div v-else-if="logs.length === 0" class="empty-state">
        <i class="fas fa-history"></i>
        <h3>Записи не найдены</h3>
      </div>

      <div v-else class="table-wrapper">
        <table class="audit-table">
          <thead>
          <tr>
            <th>Дата и время</th>
            <th>Пользователь</th>
            <th>Действие</th>
            <th>Объект</th>
            <th>IP-адрес</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td class="col-date">{{ formatDateTime(log.created_at) }}</td>
            <td>
              <div class="user-cell">
                <div class="user-avatar">{{ getInitials(log.user_name) }}</div>
                <span>{{ log.user_name }}</span>
              </div>
            </td>
            <td>
                <span class="action-badge" :class="getActionClass(log.action)">
                  {{ getActionLabel(log.action) }}
                </span>
            </td>
            <td>{{ log.target }}</td>
            <td class="col-ip">{{ log.ip }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { auditApi } from '@/api/audit.api'

const isLoading = ref(true)
const logs = ref([])
const filters = reactive({ user: '', action: '' })
let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(loadLogs, 300)
}

function resetFilters() {
  filters.user = ''
  filters.action = ''
  loadLogs()
}

async function loadLogs() {
  isLoading.value = true
  try {
    const params = {}
    if (filters.user) params.user = filters.user
    if (filters.action) params.action = filters.action
    logs.value = await auditApi.getMockLogs(params)
  } finally {
    isLoading.value = false
  }
}

function formatDateTime(dateStr) {
  return new Date(dateStr).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getInitials(name) {
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

function getActionLabel(action) {
  const labels = {
    user_blocked: 'Блокировка',
    problem_approved: 'Одобрение',
    report_rejected: 'Отклонение',
    category_created: 'Создание',
    settings_updated: 'Изменение'
  }
  return labels[action] || action
}

function getActionClass(action) {
  if (action.includes('blocked') || action.includes('rejected')) return 'action-danger'
  if (action.includes('approved') || action.includes('created')) return 'action-success'
  return 'action-info'
}

onMounted(() => loadLogs())
</script>

<style scoped lang="scss">
.audit-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

.filters-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; }
.filters-grid { display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; }
.filter-group { display: flex; flex-direction: column; }
.filter-label { display: block; margin-bottom: 0.45rem; color: #172f40; font-size: 0.82rem; font-weight: 700; }
.input-wrapper { display: flex; align-items: center; border: 1px solid #e8edf0; border-radius: 12px; background: #fcfcfd; transition: all 180ms ease; overflow: hidden; }
.input-wrapper:focus-within { border-color: #00a896; background: white; box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1); }
.input-icon { display: flex; align-items: center; justify-content: center; width: 42px; flex-shrink: 0; color: #70808c; }
.form-control-custom { flex: 1; border: none; background: transparent; padding: 0.75rem 1rem 0.75rem 0; color: #172f40; font-size: 0.9rem; width: 100%; outline: none; }
.btn-reset { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; background: #f1f5f9; border: 1px solid #e8edf0; border-radius: 12px; color: #172f40; font-size: 0.88rem; font-weight: 700; cursor: pointer; }
.btn-reset:hover { background: #e2e8f0; }

.table-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; overflow: hidden; }
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; color: #70808c; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state i { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; }

.table-wrapper { overflow-x: auto; }
.audit-table { width: 100%; border-collapse: collapse; }
.audit-table th, .audit-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.audit-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.audit-table tbody tr:hover { background: #f8fafc; }

.col-date { color: #70808c; font-size: 0.85rem; white-space: nowrap; }
.col-ip { color: #70808c; font-size: 0.85rem; font-family: monospace; }

.user-cell { display: flex; align-items: center; gap: 0.75rem; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #00a896, #087e8b); color: white; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700; flex-shrink: 0; }

.action-badge { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; }
.action-danger { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.action-success { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.action-info { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }

@media (max-width: 767.98px) {
  .filters-grid { grid-template-columns: 1fr; }
  .audit-table th:nth-child(5), .audit-table td:nth-child(5) { display: none; }
}
</style>