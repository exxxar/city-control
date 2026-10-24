<!-- admin/src/views/initiatives/InitiativesView.vue -->
<template>
  <div class="initiatives-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Инициативы граждан</h1>
        <p class="page-subtitle">Модерация и контроль реализации предложений жителей</p>
      </div>
      <div class="page-stats">
        <div class="stat-badge stat-badge--warning">
          <i class="fas fa-clock"></i>
          <span>На модерации: {{ initiativesStore.pendingCount }}</span>
        </div>
        <div class="stat-badge stat-badge--success">
          <i class="fas fa-check-double"></i>
          <span>Реализовано: {{ initiativesStore.implementedCount }}</span>
        </div>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="initiativesStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные.</span>
      </div>
    </Transition>

    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Поиск</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-search"></i></span>
            <input v-model="filters.search" type="text" class="form-control-custom" placeholder="Название или автор" @input="debouncedSearch">
          </div>
        </div>
        <div class="filter-group">
          <label class="filter-label">Статус</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-filter"></i></span>
            <select v-model="filters.status" class="form-control-custom" @change="applyFilters">
              <option value="">Все статусы</option>
              <option value="pending">⏳ На модерации</option>
              <option value="approved">✅ Одобрены (голосование)</option>
              <option value="implemented">🏆 Реализованы</option>
              <option value="rejected">❌ Отклонены</option>
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
      <div v-if="initiativesStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка инициатив...</p>
      </div>

      <div v-else-if="initiativesStore.initiatives.length === 0" class="empty-state">
        <i class="fas fa-lightbulb"></i>
        <h3>Инициативы не найдены</h3>
      </div>

      <div v-else class="table-wrapper">
        <table class="initiatives-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>Инициатива</th>
            <th>Автор</th>
            <th>Голоса</th>
            <th>Статус</th>
            <th>Дата</th>
            <th class="actions-column">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in initiativesStore.initiatives" :key="item.id">
            <td class="col-id">#{{ item.id }}</td>
            <td>
              <div class="title-cell">
                <div class="title">{{ item.title }}</div>
                <div class="category">{{ item.category }}</div>
              </div>
            </td>
            <td>{{ item.author }}</td>
            <td>
              <div class="votes-cell">
                <span class="vote-up"><i class="fas fa-thumbs-up"></i> {{ item.votes_up }}</span>
                <span class="vote-down"><i class="fas fa-thumbs-down"></i> {{ item.votes_down }}</span>
              </div>
            </td>
            <td>
                <span class="status-badge" :class="`status-${item.status}`">
                  {{ getStatusLabel(item.status) }}
                </span>
            </td>
            <td class="col-date">{{ formatDate(item.created_at) }}</td>
            <td>
              <button class="action-btn action-btn--primary" @click="openDetailModal(item)" title="Подробнее">
                <i class="fas fa-eye"></i>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <div v-if="initiativesStore.pagination.pages > 1" class="pagination">
        <button class="pagination-btn" :disabled="initiativesStore.pagination.page === 1" @click="goToPage(initiativesStore.pagination.page - 1)">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="pagination-info">Стр. {{ initiativesStore.pagination.page }} из {{ initiativesStore.pagination.pages }}</span>
        <button class="pagination-btn" :disabled="initiativesStore.pagination.page === initiativesStore.pagination.pages" @click="goToPage(initiativesStore.pagination.page + 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <InitiativeDetailModal
        v-if="selectedItem"
        :item="selectedItem"
        @close="selectedItem = null"
        @updated="onItemUpdated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useInitiativesStore } from '@/stores/initiatives.store'
import { useNotifications } from '@/composables/useNotifications'
import InitiativeDetailModal from '@/components/initiatives/InitiativeDetailModal.vue'

const initiativesStore = useInitiativesStore()
const { success } = useNotifications()

const filters = reactive({ search: '', status: '' })
const selectedItem = ref(null)
let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(applyFilters, 300)
}

function applyFilters() {
  initiativesStore.pagination.page = 1
  loadInitiatives()
}

function resetFilters() {
  filters.search = ''
  filters.status = ''
  applyFilters()
}

function goToPage(page) {
  initiativesStore.pagination.page = page
  loadInitiatives()
}

async function loadInitiatives() {
  const params = { page: initiativesStore.pagination.page, per_page: initiativesStore.pagination.per_page }
  if (filters.search) params.search = filters.search
  if (filters.status) params.status = filters.status
  await initiativesStore.fetchInitiatives(params)
}

function getStatusLabel(status) {
  const labels = { pending: 'На модерации', approved: 'Одобрена', implemented: 'Реализована', rejected: 'Отклонена' }
  return labels[status] || status
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

function openDetailModal(item) {
  selectedItem.value = { ...item }
}

async function onItemUpdated() {
  selectedItem.value = null
  await loadInitiatives()
  success('Статус инициативы обновлен')
}

onMounted(() => loadInitiatives())
</script>

<style scoped lang="scss">
// Используем те же стили, что и в ProblemsView, плюс специфичные:
.initiatives-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }
.page-stats { display: flex; gap: 0.75rem; }
.stat-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.85rem; font-weight: 700; }
.stat-badge--warning { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.stat-badge--success { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.filters-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; }
.filters-grid { display: grid; grid-template-columns: 2fr 1fr auto; gap: 1rem; }
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
.initiatives-table { width: 100%; border-collapse: collapse; }
.initiatives-table th, .initiatives-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.initiatives-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.initiatives-table tbody tr:hover { background: #f8fafc; }
.col-id { font-weight: 700; color: #70808c; font-size: 0.85rem; }

.title-cell .title { font-weight: 700; color: #172f40; font-size: 0.92rem; margin-bottom: 0.25rem; }
.title-cell .category { color: #70808c; font-size: 0.78rem; }

.votes-cell { display: flex; gap: 0.75rem; font-size: 0.85rem; font-weight: 600; }
.vote-up { color: #06d6a0; }
.vote-down { color: #c64752; }

.status-badge { display: inline-flex; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; }
.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-approved { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }
.status-implemented { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }

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
  .initiatives-table th:nth-child(3), .initiatives-table td:nth-child(3),
  .initiatives-table th:nth-child(6), .initiatives-table td:nth-child(6) { display: none; }
}
</style>