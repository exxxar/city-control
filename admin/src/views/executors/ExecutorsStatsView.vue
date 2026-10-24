<!-- admin/src/views/executors/ExecutorsStatsView.vue -->
<template>
  <div class="executors-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Статистика исполнителей</h1>
        <p class="page-subtitle">Рейтинг и аналитика работы сотрудников</p>
      </div>
      <div class="page-stats">
        <div class="stat-badge stat-badge--success">
          <i class="fas fa-check-circle"></i>
          <span>Всего закрыто: {{ executorsStore.totalCompleted }}</span>
        </div>
        <div class="stat-badge stat-badge--primary">
          <i class="fas fa-star"></i>
          <span>Средний рейтинг: {{ executorsStore.avgRating }}</span>
        </div>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="executorsStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные.</span>
      </div>
    </Transition>

    <!-- Топ-3 исполнителя -->
    <div class="top-performers">
      <h2 class="section-title">
        <i class="fas fa-trophy"></i>
        Лучшие исполнители
      </h2>
      <div class="performers-grid">
        <div v-for="(executor, index) in executorsStore.topPerformers" :key="executor.id" class="performer-card" :class="`performer-${index + 1}`">
          <div class="performer-rank">
            <i :class="getMedalIcon(index)"></i>
          </div>
          <div class="performer-info">
            <div class="performer-name">{{ executor.full_name }}</div>
            <div class="performer-dept">{{ executor.department }}</div>
          </div>
          <div class="performer-stats">
            <div class="performer-rating">
              <i class="fas fa-star"></i>
              <span>{{ executor.rating }}</span>
            </div>
            <div class="performer-completed">{{ executor.completed }} закрыто</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица всех исполнителей -->
    <div class="table-card">
      <div class="table-header">
        <h2 class="table-title">Все исполнители</h2>
        <button class="btn-export" @click="handleExport">
          <i class="fas fa-file-excel"></i>
          Экспорт
        </button>
      </div>

      <div v-if="executorsStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка статистики...</p>
      </div>

      <div v-else class="table-wrapper">
        <table class="executors-table">
          <thead>
          <tr>
            <th>Исполнитель</th>
            <th>Отдел</th>
            <th>Назначено</th>
            <th>Закрыто</th>
            <th>В работе</th>
            <th>Просрочено</th>
            <th>Ср. время (дн.)</th>
            <th>Рейтинг</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="executor in executorsStore.stats" :key="executor.id">
            <td>
              <div class="executor-cell">
                <div class="executor-avatar">{{ getInitials(executor.full_name) }}</div>
                <div class="executor-name">{{ executor.full_name }}</div>
              </div>
            </td>
            <td><span class="dept-badge">{{ executor.department }}</span></td>
            <td class="num-cell">{{ executor.total_assigned }}</td>
            <td class="num-cell num-cell--success">{{ executor.completed }}</td>
            <td class="num-cell num-cell--warning">{{ executor.in_progress }}</td>
            <td class="num-cell num-cell--danger">{{ executor.overdue }}</td>
            <td class="num-cell">{{ executor.avg_resolution_time }}</td>
            <td>
              <div class="rating-cell">
                <i class="fas fa-star"></i>
                <span>{{ executor.rating }}</span>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useExecutorsStore } from '@/stores/executors.store'
import { useExport } from '@/composables/useExport'

const executorsStore = useExecutorsStore()
const { exportToExcel } = useExport()

function getInitials(fullName) {
  if (!fullName) return '?'
  return fullName.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

function getMedalIcon(index) {
  const medals = ['fas fa-crown', 'fas fa-medal', 'fas fa-award']
  return medals[index] || 'fas fa-star'
}

function handleExport() {
  exportToExcel(
      executorsStore.stats,
      'статистика_исполнителей',
      'Исполнители',
      {
        full_name: 'ФИО',
        department: 'Отдел',
        total_assigned: 'Назначено',
        completed: 'Закрыто',
        in_progress: 'В работе',
        overdue: 'Просрочено',
        avg_resolution_time: 'Ср. время (дн.)',
        rating: 'Рейтинг'
      }
  )
}

onMounted(() => {
  executorsStore.fetchStats()
})
</script>

<style scoped lang="scss">
.executors-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }
.page-stats { display: flex; gap: 0.75rem; }

.stat-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.85rem; font-weight: 700; }
.stat-badge--success { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.stat-badge--primary { background: rgba(0, 168, 150, 0.12); color: #00a896; }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.top-performers { background: white; border: 1px solid #e8edf0; border-radius: 20px; padding: 1.75rem; }
.section-title { display: flex; align-items: center; gap: 0.75rem; margin: 0 0 1.5rem; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.section-title i { color: #fbbf24; font-size: 1.3rem; }

.performers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
.performer-card { display: flex; align-items: center; gap: 1rem; padding: 1.25rem; border-radius: 16px; border: 2px solid; transition: all 0.2s ease; }
.performer-card:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(23, 47, 64, 0.1); }

.performer-1 { border-color: #fbbf24; background: linear-gradient(135deg, rgba(251, 191, 36, 0.05), rgba(251, 191, 36, 0.02)); }
.performer-2 { border-color: #94a3b8; background: linear-gradient(135deg, rgba(148, 163, 184, 0.05), rgba(148, 163, 184, 0.02)); }
.performer-3 { border-color: #d97706; background: linear-gradient(135deg, rgba(217, 119, 6, 0.05), rgba(217, 119, 6, 0.02)); }

.performer-rank { font-size: 2rem; flex-shrink: 0; }
.performer-1 .performer-rank { color: #fbbf24; }
.performer-2 .performer-rank { color: #94a3b8; }
.performer-3 .performer-rank { color: #d97706; }

.performer-info { flex: 1; min-width: 0; }
.performer-name { font-weight: 700; color: #172f40; font-size: 0.95rem; margin-bottom: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.performer-dept { color: #70808c; font-size: 0.82rem; }

.performer-stats { text-align: right; }
.performer-rating { display: flex; align-items: center; gap: 0.35rem; font-weight: 800; color: #fbbf24; font-size: 1.1rem; margin-bottom: 0.25rem; }
.performer-completed { color: #06d6a0; font-size: 0.82rem; font-weight: 600; }

.table-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; overflow: hidden; }
.table-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e8edf0; }
.table-title { margin: 0; font-size: 1.1rem; font-weight: 800; color: #172f40; }

.btn-export { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.65rem 1.25rem; background: linear-gradient(135deg, #1d6f42, #155732); color: white; border: none; border-radius: 12px; font-size: 0.88rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(29, 111, 66, 0.25); }
.btn-export:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(29, 111, 66, 0.35); }
.btn-export i { color: #a3e635; }

.loading-state { display: flex; flex-direction: column; align-items: center; padding: 4rem 2rem; color: #70808c; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }

.table-wrapper { overflow-x: auto; }
.executors-table { width: 100%; border-collapse: collapse; }
.executors-table th, .executors-table td { padding: 1rem 1.25rem; text-align: left; border-bottom: 1px solid #f1f5f9; }
.executors-table th { background: #f8fafc; font-size: 0.78rem; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; }
.executors-table tbody tr:hover { background: #f8fafc; }

.executor-cell { display: flex; align-items: center; gap: 0.75rem; }
.executor-avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #00a896, #087e8b); color: white; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; flex-shrink: 0; }
.executor-name { font-weight: 600; color: #172f40; font-size: 0.9rem; }

.dept-badge { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 8px; background: rgba(13, 202, 240, 0.12); color: #0dcaf0; font-size: 0.78rem; font-weight: 700; }

.num-cell { font-weight: 700; color: #172f40; font-size: 0.95rem; }
.num-cell--success { color: #06d6a0; }
.num-cell--warning { color: #fd7e14; }
.num-cell--danger { color: #c64752; }

.rating-cell { display: flex; align-items: center; gap: 0.35rem; font-weight: 800; color: #fbbf24; font-size: 1rem; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 767.98px) {
  .performers-grid { grid-template-columns: 1fr; }
  .executors-table th:nth-child(7), .executors-table td:nth-child(7) { display: none; }
}
</style>