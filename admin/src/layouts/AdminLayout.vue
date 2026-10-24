<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-brand">
        <i class="fa-solid fa-shield-halved"></i>
        <span>Админ-панель</span>
      </div>

      <nav class="sidebar-nav">
        <router-link
            v-for="item in visibleMenuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            active-class="active"
        >
          <i :class="`fa-solid ${item.icon}`"></i>
          <span>{{ item.title }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="logout-btn" @click="handleLogout">
          <i class="fa-solid fa-right-from-bracket"></i>
          <span>Выйти</span>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="admin-main">
      <header class="admin-header">
        <div class="header-breadcrumb">
          <h1>{{ currentRoute.meta.title || 'Админ-панель' }}</h1>
        </div>
        <button class="theme-toggle" @click="toggleTheme" :title="isDark ? 'Светлая тема' : 'Тёмная тема'">
          <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
        </button>
        <NotificationsDropdown />
        <div class="header-user" v-if="authStore.user">
          <div class="user-avatar">
            <i class="fa-solid fa-user"></i>
          </div>
          <div class="user-info">
            <div class="user-name">{{ authStore.user.full_name || 'Администратор' }}</div>
            <div class="user-role">
              {{ authStore.user.roles?.[0]?.name || 'Администратор' }}
            </div>
          </div>
        </div>
      </header>

      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import NotificationsDropdown from '@/components/notifications/NotificationsDropdown.vue'
import { useTheme } from '@/composables/useTheme'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()
const currentRoute = computed(() => route)

// Полный список всех возможных пунктов меню с указанием требуемых ролей
const allMenuItems = [
  { path: '/dashboard', title: 'Дашборд', icon: 'fa-chart-line', roles: ['Системный администратор', 'Руководитель органа', 'Модератор'] },
  { path: '/problems', title: 'Обращения', icon: 'fa-triangle-exclamation', roles: ['Системный администратор', 'Модератор'] },
  { path: '/initiatives', title: 'Инициативы', icon: 'fa-lightbulb', roles: ['Системный администратор', 'Модератор'] },
  { path: '/events', title: 'Мероприятия', icon: 'fa-calendar-days', roles: ['Системный администратор', 'Модератор'] },
  { path: '/reports', title: 'Отчёты', icon: 'fa-file-lines', roles: ['Системный администратор', 'Руководитель органа', 'Модератор'] },
  { path: '/users', title: 'Пользователи', icon: 'fa-users', roles: ['Системный администратор'] },
  { path: '/roles', title: 'Роли', icon: 'fa-user-shield', roles: ['Системный администратор'] },
  { path: '/issue-categories', title: 'Категории', icon: 'fa-tags', roles: ['Системный администратор'] },
  { path: '/executors', title: 'Исполнители', icon: 'fa-chart-simple', roles: ['Системный администратор', 'Руководитель органа'] },
  { path: '/audit', title: 'Журнал', icon: 'fa-history', roles: ['Системный администратор'] },
  { path: '/settings', title: 'Настройки', icon: 'fa-gear', roles: ['Системный администратор'] }
]

// Фильтруем меню: показываем только те пункты, на которые у пользователя есть права
const visibleMenuItems = computed(() => {
  const userRoles = authStore.user?.roles?.map(r => r.name) || []

  return allMenuItems.filter(item =>
      item.roles.some(role => userRoles.includes(role))
  )
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f8fa;
}

.admin-sidebar {
  width: 260px;
  background: #172f40;
  color: white;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 100;
}

.sidebar-brand {
  padding: 1.5rem;
  font-size: 1.25rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);

  i {
    color: #00a896;
    font-size: 1.5rem;
  }
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.2s;

  &:hover {
    background: rgba(255,255,255,0.08);
    color: white;
  }

  &.active {
    background: linear-gradient(135deg, #00a896, #087e8b);
    color: white;
    box-shadow: 0 4px 12px rgba(0, 168, 150, 0.3);
  }

  i {
    width: 20px;
    text-align: center;
  }
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.logout-btn {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: all 0.2s;

  &:hover {
    background: rgba(198, 71, 82, 0.2);
    border-color: #c64752;
  }
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-header {
  background: white;
  padding: 1rem 2rem;
  border-bottom: 1px solid #e8edf0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-breadcrumb h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
  color: #172f40;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.user-info {
  text-align: right;
}

.user-name {
  font-weight: 700;
  color: #172f40;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.75rem;
  color: #70808c;
}

.admin-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* Адаптивность для мобильных */
@media (max-width: 767.98px) {
  .admin-sidebar {
    position: fixed;
    left: -260px;
    transition: left 0.3s ease;

    &.open {
      left: 0;
    }
  }

  .admin-header {
    padding: 1rem;
  }

  .admin-content {
    padding: 1rem;
  }
}

.theme-toggle {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid #e8edf0;
  background: white;
  color: #70808c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;

  &:hover {
    background: #f8fafc;
    color: #fbbf24;
    border-color: #fbbf24;
  }
}

.dark-theme .theme-toggle {
  background: #172f40;
  border-color: #2d4a5e;
  color: #70808c;

  &:hover {
    background: #0a141e;
    color: #fbbf24;
  }
}
</style>