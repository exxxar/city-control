import { createRouter, createWebHistory } from 'vue-router'
import { setupGuards } from './guards'
import AdminLayout from '@/layouts/AdminLayout.vue'

const routes = [
  // === Авторизация ===
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guestOnly: true, title: 'Вход в админку' }
  },

  // === Защищённые разделы ===
  {
    path: '/',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('@/views/roles/RolesView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Роли и разрешения',
          icon: 'fa-user-shield',
          roles: ['Системный администратор']
        }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/reports/ReportsView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Отчеты',
          icon: 'fa-user-shield',
          roles: ['Системный администратор']
        }
      },
      {
        path: 'issue-categories',
        name: 'IssueCategories',
        component: () => import('@/views/categories/IssueCategoriesView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Категории обращений',
          icon: 'fa-tags',
          roles: ['Системный администратор']
        }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/SettingsView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Настройки',
          icon: 'fa-gear',
          roles: ['Системный администратор']
        }
      },
      // admin/src/router/index.js (внутри children маршрута '/')

      {
        path: 'initiatives',
        name: 'Initiatives',
        component: () => import('@/views/initiatives/InitiativesView.vue'),
         meta: {
          requiresAuth: true,
          title: 'Инициативы',
          icon: 'fa-lightbulb',
          roles: ['Системный администратор', 'Модератор']
        }
      },
      {
        path: 'executors',
        name: 'ExecutorsStats',
        component: () => import('@/views/executors/ExecutorsStatsView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Статистика исполнителей',
          icon: 'fa-chart-simple',
          roles: ['Системный администратор', 'Руководитель органа']
        }
      },
      {
        path: 'audit',
        name: 'AuditLog',
        component: () => import('@/views/audit/AuditLogView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Журнал действий',
          icon: 'fa-history',
          roles: ['Системный администратор']
        }
      },
      {
        path: 'events',
        name: 'Events',
        component: () => import('@/views/events/EventsView.vue'),
        meta: { requiresAuth: true, title: 'Мероприятия', icon: 'fa-calendar-days', roles: ['Системный администратор', 'Модератор'] }
      },

      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Дашборд',
          icon: 'fa-chart-line',
          roles: ['Системный администратор', 'Руководитель органа', 'Модератор']
        }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/UsersView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Пользователи',
          icon: 'fa-users',
          roles: ['Системный администратор']
        }
      },
      {
        path: 'problems',
        name: 'Problems',
        component: () => import('@/views/problems/ProblemsView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Проблемы',
          icon: 'fa-triangle-exclamation',
          roles: ['Системный администратор', 'Модератор']
        }
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/views/categories/CategoriesView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Справочники',
          icon: 'fa-tags',
          roles: ['Системный администратор']
        }
      }
    ]
  },

  // === 403 Forbidden ===
  {
    path: '/forbidden',
    name: 'Forbidden',
    component: { template: '<div style="padding:2rem">Доступ запрещён</div>' }
  },

  // === 404 ===
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: { template: '<div style="padding:2rem">Страница не найдена</div>' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

setupGuards(router)

export default router