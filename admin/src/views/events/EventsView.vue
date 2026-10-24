<!-- admin/src/views/events/EventsView.vue -->
<template>
  <div class="events-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Мероприятия</h1>
        <p class="page-subtitle">Модерация и контроль городских событий</p>
      </div>
      <div class="page-stats">
        <div class="stat-badge stat-badge--warning">
          <i class="fas fa-clock"></i>
          <span>На согласовании: {{ pendingCount }}</span>
        </div>
        <div class="stat-badge stat-badge--success">
          <i class="fas fa-check"></i>
          <span>Согласовано: {{ approvedCount }}</span>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Поиск</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-search"></i></span>
            <input v-model="filters.search" type="text" class="form-control-custom" placeholder="Название, организатор или место" @input="debouncedSearch">
          </div>
        </div>
        <div class="filter-group">
          <label class="filter-label">Статус</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-filter"></i></span>
            <select v-model="filters.status" class="form-control-custom" @change="applyFilters">
              <option value="">Все статусы</option>
              <option value="pending">⏳ На согласовании</option>
              <option value="approved">✅ Согласовано</option>
              <option value="completed">🎉 Завершено</option>
              <option value="rejected">❌ Отклонено</option>
            </select>
          </div>
        </div>
        <div class="filter-group">
          <label class="filter-label">&nbsp;</label>
          <button class="btn-reset" @click="resetFilters"><i class="fas fa-rotate-left"></i> Сбросить</button>
        </div>
      </div>
    </div>

    <!-- Таблица -->
    <div class="table-card">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка мероприятий...</p>
      </div>

      <div v-else-if="events.length === 0" class="empty-state">
        <i class="fas fa-calendar-xmark"></i>
        <h3>Мероприятия не найдены</h3>
      </div>

      <div v-else class="table-wrapper">
        <table class="events-table">
          <thead>
          <tr>
            <th>Название</th>
            <th>Организатор</th>
            <th>Дата проведения</th>
            <th>Участников</th>
            <th>Статус</th>
            <th class="actions-column">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="event in events" :key="event.id">
            <td>
              <div class="title-cell">
                <div class="title">{{ event.title }}</div>
                <div class="location"><i class="fas fa-location-dot"></i> {{ event.location }}</div>
              </div>
            </td>
            <td>
              <div class="organizer-cell">
                <div>{{ event.organizer }}</div>
                <div class="phone">{{ event.organizer_phone }}</div>
              </div>
            </td>
            <td class="col-date">{{ formatDate(event.event_date) }}</td>
            <td>
                <span class="participants-badge">
                  <i class="fas fa-users"></i> {{ event.participants_count }}
                </span>
            </td>
            <td>
                <span class="status-badge" :class="`status-${event.status}`">
                  {{ event.statusText }}
                </span>
            </td>
            <td>
              <button class="action-btn action-btn--primary" @click="openDetailModal(event)" title="Подробнее">
                <i class="fas fa-eye"></i>
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <div v-if="pagination.pages > 1" class="pagination">
        <button class="pagination-btn" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="pagination-info">Стр. {{ pagination.page }} из {{ pagination.pages }}</span>
        <button class="pagination-btn" :disabled="pagination.page === pagination.pages" @click="goToPage(pagination.page + 1)">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Модальное окно -->
    <EventDetailModal
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="selectedEvent = null"
        @updated="onEventUpdated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import http from '@/api/http'
import { useNotifications } from '@/composables/useNotifications'
import EventDetailModal from '@/components/events/EventDetailModal.vue'

const { success } = useNotifications()

const isLoading = ref(true)
const events = ref([])
const selectedEvent = ref(null)
const pagination = reactive({ page: 1, per_page: 20, pages: 0, total: 0 })
const filters = reactive({ search: '', status: '' })
let searchTimeout = null

const pendingCount = computed(() => events.value.filter(e => e.status === 'pending').length)
const approvedCount = computed(() => events.value.filter(e => e.status === 'approved').length)

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(loadEvents, 300)
}

function applyFilters() {
  pagination.page = 1
  loadEvents()
}

function resetFilters() {
  filters.search = ''
  filters.status = ''
  applyFilters()
}

function goToPage(page) {
  pagination.page = page
  loadEvents()
}

async function loadEvents() {
  isLoading.value = true
  try {
    const params = { page: pagination.page, per_page: pagination.per_page }
    if (filters.search) params.search = filters.search
    if (filters.status) params.status = filters.status

    const response = await http.get('/admin/events', { params })
    events.value = response.data.items || response.data
    pagination.page = response.data.page || 1
    pagination.pages = response.data.pages || 0
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('Load events error:', error)
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function openDetailModal(event) {
  selectedEvent.value = { ...event }
}

async function onEventUpdated() {
  selectedEvent.value = null
  await loadEvents()
  success('Статус мероприятия обновлен')
}

onMounted(() => loadEvents())
</script>

<style scoped lang="scss">
.events-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }
.page-stats { display: flex; gap: 0.75rem; }
.stat-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.85rem; font-weight: 700; }
.stat-badge--warning { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.stat-badge--success { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }

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
.events-table { width: 100%; border-collapse: collapse; }
.events-table th, .events-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.events-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.events-table tbody tr:hover { background: #f8fafc; }

.title-cell .title { font-weight: 700; color: #172f40; font-size: 0.92rem; margin-bottom: 0.25rem; }
.title-cell .location { color: #70808c; font-size: 0.78rem; display: flex; align-items: center; gap: 0.35rem; }

.organizer-cell { font-size: 0.9rem; color: #172f40; font-weight: 600; }
.organizer-cell .phone { font-size: 0.78rem; color: #70808c; font-weight: 400; margin-top: 0.15rem; }

.col-date { color: #70808c; font-size: 0.85rem; white-space: nowrap; }

.participants-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.35rem 0.75rem; background: rgba(0, 168, 150, 0.12); color: #00a896; border-radius: 8px; font-size: 0.85rem; font-weight: 700; }

.status-badge { display: inline-flex; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700; }
.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-completed { background: rgba(113, 128, 150, 0.12); color: #70808c; }
.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }

.actions-column { width: 80px; }
.action-btn { width: 36px; height: 36px; border-radius: 10px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; transition: all 0.2s ease; }
.action-btn--primary { background: rgba(0, 168, 150, 0.12); color: #00a896; }
.action-btn--primary:hover { background: #00a896; color: white; }

.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; padding: 1.25rem; border-top: 1px solid #e8edf0; }
.pagination-btn { width: 36px; height: 36px; border-radius: 10px; border: 1px solid #e8edf0; background: white; color: #172f40; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.pagination-btn:hover:not(:disabled) { background: #f8fafc; border-color: #00a896; color: #00a896; }
.pagination-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination-info { color: #70808c; font-size: 0.88rem; font-weight: 600; }

@media (max-width: 991.98px) {
  .filters-grid { grid-template-columns: 1fr; }
  .events-table th:nth-child(4), .events-table td:nth-child(4) { display: none; }
}
</style>