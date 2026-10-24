<!-- admin/src/views/dashboard/DashboardView.vue -->
<template>
  <div class="dashboard">
    <!-- Приветствие -->
    <div class="welcome-banner">
      <div class="welcome-content">
        <h1 class="welcome-title">Добро пожаловать, {{ authStore.user?.full_name?.split(' ')[0] || 'Администратор' }} 👋</h1>
        <p class="welcome-subtitle">Сводка по работе муниципального сервиса за сегодня</p>
      </div>
      <div class="welcome-date">
        <i class="fas fa-calendar-day"></i>
        {{ currentDate }}
      </div>
    </div>

    <!-- Карточки статистики -->
    <div class="stats-grid">
      <div class="stat-card stat-card--primary">
        <div class="stat-icon"><i class="fas fa-users"></i></div>
        <div class="stat-info">
          <div class="stat-label">Пользователей</div>
          <div class="stat-value">{{ formatNumber(dashboardStore.stats.totalUsers) }}</div>
        </div>
      </div>
      <div class="stat-card stat-card--danger">
        <div class="stat-icon"><i class="fas fa-triangle-exclamation"></i></div>
        <div class="stat-info">
          <div class="stat-label">Новых проблем</div>
          <div class="stat-value">{{ dashboardStore.stats.newProblems }}</div>
          <div class="stat-trend">
            <span class="trend-label">сегодня:</span>
            <span class="trend-value">{{ dashboardStore.stats.todayNewProblems }}</span>
          </div>
        </div>
      </div>
      <div class="stat-card stat-card--warning">
        <div class="stat-icon"><i class="fas fa-spinner"></i></div>
        <div class="stat-info">
          <div class="stat-label">В работе</div>
          <div class="stat-value">{{ dashboardStore.stats.inProgressProblems }}</div>
        </div>
      </div>
      <div class="stat-card stat-card--success">
        <div class="stat-icon"><i class="fas fa-circle-check"></i></div>
        <div class="stat-info">
          <div class="stat-label">Решено</div>
          <div class="stat-value">{{ dashboardStore.stats.resolvedProblems }}</div>
          <div class="stat-trend">
            <span class="trend-label">эффективность:</span>
            <span class="trend-value trend-value--good">{{ dashboardStore.resolutionRate }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Графики -->
    <div class="charts-grid">
      <!-- Круговая диаграмма: Статусы проблем -->
      <div class="chart-card">
        <h3 class="chart-title">Распределение проблем по статусам</h3>
        <div class="chart-container">
          <Doughnut :data="statusChartData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- Столбчатая диаграмма: Категории -->
      <div class="chart-card">
        <h3 class="chart-title">Топ категорий обращений</h3>
        <div class="chart-container">
          <Bar :data="categoryChartData" :options="barOptions" />
        </div>
      </div>
    </div>

    <!-- Последние проблемы -->
    <div class="dashboard-card recent-problems-card">
      <div class="card-header">
        <div>
          <h2 class="card-title">Последние обращения</h2>
          <p class="card-subtitle">Требуют внимания модератора</p>
        </div>
        <router-link to="/problems" class="card-action">
          Все обращения <i class="fas fa-arrow-right"></i>
        </router-link>
      </div>
      <div class="problems-list">
        <div
            v-for="problem in dashboardStore.recentProblems.slice(0, 5)"
            :key="problem.id"
            class="problem-item"
        >
          <div class="problem-status" :class="`status--${problem.status}`"></div>
          <div class="problem-content">
            <div class="problem-title">{{ problem.title }}</div>
            <div class="problem-meta">
              <span class="meta-item"><i class="fas fa-tag"></i> {{ problem.category }}</span>
              <span class="meta-item"><i class="fas fa-location-dot"></i> {{ problem.address }}</span>
            </div>
          </div>
          <div class="problem-date">{{ formatDate(problem.created_at) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useDashboardStore } from '@/stores/dashboard.store'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

// Регистрируем компоненты Chart.js
ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement
)

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const currentDate = computed(() =>
    new Date().toLocaleDateString('ru-RU', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
)

function formatNumber(num) {
  return num ? num.toLocaleString('ru-RU') : '0'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const diffHours = Math.floor((new Date() - new Date(dateStr)) / (1000 * 60 * 60))
  if (diffHours < 1) return 'только что'
  if (diffHours < 24) return `${diffHours} ч. назад`
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

// Данные для круговой диаграммы
const statusChartData = computed(() => ({
  labels: ['Новые', 'В работе', 'Решены', 'Отклонены'],
  datasets: [{
    data: [
      dashboardStore.stats.newProblems || 47,
      dashboardStore.stats.inProgressProblems || 128,
      dashboardStore.stats.resolvedProblems || 717,
      35
    ],
    backgroundColor: ['#fd7e14', '#0dcaf0', '#06d6a0', '#c64752'],
    borderWidth: 0,
    hoverOffset: 4
  }]
}))

// Данные для столбчатой диаграммы
const categoryChartData = computed(() => ({
  labels: ['ЖКХ', 'Дороги', 'Благоустройство', 'Экология', 'Транспорт'],
  datasets: [{
    label: 'Количество обращений',
    data: [320, 215, 180, 95, 82],
    backgroundColor: '#00a896',
    borderRadius: 6,
    barThickness: 30
  }]
}))

// Опции для круговой диаграммы
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: { family: 'sans-serif', size: 12 }
      }
    }
  },
  cutout: '65%'
}

// Опции для столбчатой диаграммы
const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9' },
      ticks: { font: { size: 11 } }
    },
    x: {
      grid: { display: false },
      ticks: { font: { size: 11 } }
    }
  }
}

onMounted(() => {
  dashboardStore.loadAll()
})
</script>

<style scoped lang="scss">
.dashboard { display: flex; flex-direction: column; gap: 1.5rem; }

.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.75rem 2rem;
  background: linear-gradient(135deg, #172f40 0%, #0f1f2b 100%);
  border-radius: 20px;
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 168, 150, 0.3) 0%, transparent 70%);
    border-radius: 50%;
  }
}

.welcome-title { margin: 0; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.03em; }
.welcome-subtitle { margin: 0.5rem 0 0; color: rgba(255, 255, 255, 0.7); font-size: 0.95rem; }
.welcome-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e8edf0;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(23, 47, 64, 0.08);
  }
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  flex-shrink: 0;
}

.stat-card--primary .stat-icon { background: rgba(0, 168, 150, 0.12); color: #00a896; }
.stat-card--danger .stat-icon { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.stat-card--warning .stat-icon { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.stat-card--success .stat-icon { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }

.stat-info { flex: 1; min-width: 0; }
.stat-label { font-size: 0.82rem; color: #70808c; font-weight: 600; margin-bottom: 0.25rem; }
.stat-value { font-size: 1.75rem; font-weight: 800; color: #172f40; letter-spacing: -0.03em; line-height: 1; }
.stat-trend { display: flex; align-items: center; gap: 0.35rem; margin-top: 0.35rem; font-size: 0.78rem; }
.trend-label { color: #70808c; }
.trend-value { font-weight: 700; color: #172f40; }
.trend-value--good { color: #06d6a0; }

.charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1.5rem; }
.chart-card { background: white; border: 1px solid #e8edf0; border-radius: 20px; padding: 1.5rem; }
.chart-title { margin: 0 0 1.5rem; font-size: 1.1rem; font-weight: 800; color: #172f40; }
.chart-container { position: relative; height: 300px; width: 100%; }

.dashboard-card { background: white; border: 1px solid #e8edf0; border-radius: 20px; overflow: hidden; }
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid #e8edf0;
}
.card-title { margin: 0; font-size: 1.15rem; font-weight: 800; color: #172f40; }
.card-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.85rem; }
.card-action {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #00a896;
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  transition: gap 0.2s ease;

  &:hover { gap: 0.75rem; }
}

.problems-list { padding: 0.5rem 0; }
.problem-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.75rem;
  transition: background 0.15s ease;

  &:hover { background: #f8fafc; }
  & + & { border-top: 1px solid #f1f5f9; }
}

.problem-status { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.status--new { background: #c64752; box-shadow: 0 0 0 4px rgba(198, 71, 82, 0.15); }
.status--in_progress { background: #fd7e14; box-shadow: 0 0 0 4px rgba(253, 126, 20, 0.15); }
.status--resolved { background: #06d6a0; box-shadow: 0 0 0 4px rgba(6, 214, 160, 0.15); }

.problem-content { flex: 1; min-width: 0; }
.problem-title {
  font-weight: 700;
  color: #172f40;
  font-size: 0.95rem;
  margin-bottom: 0.35rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.problem-meta { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  color: #70808c;
  font-size: 0.78rem;

  i { font-size: 0.7rem; }
}

.problem-date { color: #70808c; font-size: 0.78rem; font-weight: 600; white-space: nowrap; flex-shrink: 0; }

@media (max-width: 767.98px) {
  .charts-grid { grid-template-columns: 1fr; }
  .welcome-banner { flex-direction: column; align-items: flex-start; gap: 1rem; padding: 1.5rem; }
}
</style>