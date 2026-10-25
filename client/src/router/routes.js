// client/src/router/routes.js
import LandingLayout from '@/layouts/LandingLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'
import AppLayout from '@/layouts/AppLayout.vue'

export const routes = [
  // === 1. ГЛАВНАЯ - ЛЕНДИНГ (с LandingLayout) ===
  {
    path: '/',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Landing',
        component: () => import('@/views/public/LandingView.vue'),
        meta: { requiresAuth: false, title: 'Город под контролем' }
      }
    ]
  },

  // === 2. КАРТА (с LandingLayout) ===
  {
    path: '/map',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'Map',
        component: () => import('@/views/public/MapView.vue'),
        meta: { requiresAuth: false, title: 'Карта проблем' }
      }
    ]
  },

  // === 3. АВТОРИЗАЦИЯ (AuthLayout) ===
  {
    path: '/login',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('@/views/auth/LoginView.vue'),
        meta: { requiresAuth: false, title: 'Вход', guestOnly: true }
      }
    ]
  },
  {
    path: '/register',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Register',
        component: () => import('@/views/auth/RegisterView.vue'),
        meta: { requiresAuth: false, title: 'Регистрация', guestOnly: true }
      }
    ]
  },
  {
    path: '/forgot-password',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ForgotPassword',
        component: () => import('@/views/auth/ForgotPasswordView.vue'),
        meta: { requiresAuth: false, title: 'Восстановление пароля' }
      }
    ]
  },
  {
    path: '/reset-password',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ResetPassword',
        component: () => import('@/views/auth/ResetPasswordView.vue'),
        meta: { requiresAuth: false, title: 'Сброс пароля' }
      }
    ]
  },

  // === 4. ПУБЛИЧНЫЕ СТРАНИЦЫ (PublicLayout) ===
  {
    path: '/privacy',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Privacy',
        component: () => import('@/views/public/PrivacyView.vue'),
        meta: { requiresAuth: false, title: 'Политика конфиденциальности' }
      }
    ]
  },
  {
    path: '/terms',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Terms',
        component: () => import('@/views/public/TermsView.vue'),
        meta: { requiresAuth: false, title: 'Условия использования' }
      }
    ]
  },
  {
    path: '/about',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'About',
        component: () => import('@/views/public/AboutView.vue'),
        meta: { requiresAuth: false, title: 'О проекте' }
      }
    ]
  },
  {
    path: '/contacts',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Contacts',
        component: () => import('@/views/public/ContactsView.vue'),
        meta: { requiresAuth: false, title: 'Контакты' }
      }
    ]
  },
  {
    path: '/create-wizard',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ProblemCreateWizard',
        component: () => import('@/views/problems/ProblemCreateWizard.vue'),
        meta: { requiresAuth: true, title: 'Создание обращения' }
      }
    ]
  },
  {
    path: '/events/create-v2',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'EventRequestForm',
        component: () => import('@/views/events/EventRequestForm.vue'),
        meta: { requiresAuth: true, title: 'Заявка на мероприятие' }
      }
    ]
  },
  {
    path: '/reports/result',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ResultReport',
        component: () => import('@/views/reports/ResultReportView.vue'),
        meta: { requiresAuth: true, title: 'Отчёт о выполнении', roles: ['Исполнитель', 'Руководитель органа', 'Системный администратор'] }
      }
    ]
  },
  {
    path: '/problems/:id',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ProblemPublic',
        component: () => import('@/views/public/ProblemPublicView.vue'),
        meta: { requiresAuth: false, title: 'Проблема' }
      }
    ]
  },
  {
    path: '/objects/:id',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ObjectPassport',
        component: () => import('@/views/public/ObjectPassportView.vue'),
        meta: { requiresAuth: false, title: 'Паспорт объекта' }
      }
    ]
  },

  // === 5. ЗАЩИЩЁННЫЕ СТРАНИЦЫ (LandingLayout) ===
  {
    path: '/create',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'CreateProblem',
        component: () => import('@/views/problems/ProblemCreateView.vue'),
        meta: { requiresAuth: true, title: 'Сообщить о проблеме' }
      }
    ]
  },
  {
    path: '/problems',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'MyProblems',
        component: () => import('@/views/problems/MyProblemsView.vue'),
        meta: { requiresAuth: true, title: 'Мои обращения' }
      }
    ]
  },
  {
    path: '/problems/:id/details',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ProblemDetails',
        props: true,
        component: () => import('@/views/problems/ProblemDetailsView.vue'),
        meta: { requiresAuth: true, title: 'Детали проблемы' }
      }
    ]
  },
  {
    path: '/problems/:id/chat',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ProblemChat',
        component: () => import('@/views/chat/ProblemChatView.vue'),
        meta: { requiresAuth: true, title: 'Чат проблемы' }
      }
    ]
  },
  {
    path: '/notifications',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Notifications',
        component: () => import('@/views/notifications/NotificationsView.vue'),
        meta: { requiresAuth: true, title: 'Уведомления' }
      }
    ]
  },
  {
    path: '/profile',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Profile',
        component: () => import('@/views/profile/ProfileView.vue'),
        meta: { requiresAuth: true, title: 'Профиль' }
      }
    ]
  },
  {
    path: '/settings',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Settings',
        component: () => import('@/views/profile/SettingsView.vue'),
        meta: { requiresAuth: true, title: 'Настройки' }
      }
    ]
  },
  {
    path: '/initiatives/create',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'CreateInitiative',
        component: () => import('@/views/initiatives/InitiativeCreateView.vue'),
        meta: { requiresAuth: false, title: 'Создать инициативу' }
      }
    ]
  },
  {
    path: '/initiatives/list',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'InitiativesList',
        component: () => import('@/views/initiatives/InitiativesListView.vue'),
        meta: { requiresAuth: true, title: 'Создать инициативу' }
      }
    ]
  },
  {
    path: '/events/create',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'EventCreate',
        component: () => import('@/views/events/EventCreateView.vue'),
        meta: { requiresAuth: true, title: 'Создать мероприятие' }
      }
    ]
  },
  {
    path: '/events/show',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'CreateEvent',
        component: () => import('@/views/events/EventsListView.vue'),
        meta: { requiresAuth: true, title: 'Создать мероприятие' }
      }
    ]
  },
  {
    path: '/executor/dashboard',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'ExecutorDashboard',
        component: () => import('@/views/executor/ExecutorDashboardView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Панель исполнителя',
          roles: ['Исполнитель', 'Руководитель органа', 'Системный администратор']
        }
      }
    ]
  },
  {
    path: '/executor/problems',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'AssignedProblems',
        component: () => import('@/views/executor/AssignedProblemsView.vue'),
        meta: {
          requiresAuth: true,
          title: 'Назначенные проблемы',
          roles: ['Исполнитель', 'Руководитель органа', 'Системный администратор']
        }
      }
    ]
  },

  // Камера и AR
  {
    path: '/camera',
    component: LandingLayout,
    children: [
      {
        path: '',
        name: 'Camera',
        component: () => import('@/views/camera/CameraView.vue'),
        meta: { requiresAuth: true, title: 'Камера' }
      }
    ]
  },
  {
    path: '/ar',
    component: AppLayout,
    children: [
      {
        path: '',
        name: 'ARMode',
        component: () => import('@/views/ar/ARView.vue'),
        meta: { requiresAuth: true, title: 'AR-режим' }
      }
    ]
  },
  // === 6. 404 NOT FOUND ===
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/public/NotFoundView.vue'),
    meta: { requiresAuth: false, title: 'Страница не найдена' }
  }
]

export default routes