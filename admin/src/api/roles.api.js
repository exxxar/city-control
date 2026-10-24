// admin/src/api/roles.api.js
import http from './http'

// Матрица всех возможных разрешений в системе
export const ALL_PERMISSIONS = [
    { key: 'view_users', label: 'Просмотр пользователей', group: 'Пользователи' },
    { key: 'manage_users', label: 'Управление пользователями', group: 'Пользователи' },
    { key: 'view_problems', label: 'Просмотр обращений', group: 'Обращения' },
    { key: 'moderate_problems', label: 'Модерация обращений', group: 'Обращения' },
    { key: 'assign_problems', label: 'Назначение исполнителей', group: 'Обращения' },
    { key: 'view_initiatives', label: 'Просмотр инициатив', group: 'Инициативы' },
    { key: 'moderate_initiatives', label: 'Модерация инициатив', group: 'Инициативы' },
    { key: 'view_events', label: 'Просмотр мероприятий', group: 'Мероприятия' },
    { key: 'moderate_events', label: 'Модерация мероприятий', group: 'Мероприятия' },
    { key: 'view_reports', label: 'Просмотр отчётов', group: 'Отчёты' },
    { key: 'approve_reports', label: 'Принятие отчётов', group: 'Отчёты' },
    { key: 'view_categories', label: 'Просмотр справочников', group: 'Справочники' },
    { key: 'manage_categories', label: 'Управление справочниками', group: 'Справочники' },
    { key: 'view_roles', label: 'Просмотр ролей', group: 'Роли' },
    { key: 'manage_roles', label: 'Управление ролями', group: 'Роли' },
    { key: 'view_audit', label: 'Просмотр журнала', group: 'Безопасность' },
    { key: 'view_settings', label: 'Просмотр настроек', group: 'Настройки' },
    { key: 'manage_settings', label: 'Изменение настроек', group: 'Настройки' }
]

export const rolesApi = {
    getAll: () => http.get('/admin/roles').then(r => r.data),
    create: (data) => http.post('/admin/roles', data).then(r => r.data),
    update: (id, data) => http.put(`/admin/roles/${id}`, data).then(r => r.data),
    delete: (id) => http.delete(`/admin/roles/${id}`).then(r => r.data),

    // === ЗАГЛУШКИ ===
    getMockRoles: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    {
                        id: 1, name: 'Пользователь', description: 'Базовая роль для всех зарегистрированных пользователей',
                        permissions: ['view_problems', 'view_initiatives', 'view_events'],
                        is_system: true, users_count: 1180
                    },
                    {
                        id: 2, name: 'Модератор', description: 'Модерация обращений, инициатив и мероприятий',
                        permissions: ['view_users', 'view_problems', 'moderate_problems', 'view_initiatives', 'moderate_initiatives', 'view_events', 'moderate_events', 'view_reports'],
                        is_system: false, users_count: 12
                    },
                    {
                        id: 3, name: 'Исполнитель', description: 'Сотрудник, выполняющий работы по обращениям',
                        permissions: ['view_problems', 'view_reports'],
                        is_system: false, users_count: 28
                    },
                    {
                        id: 4, name: 'Руководитель органа', description: 'Руководитель подразделения с расширенными правами',
                        permissions: ['view_users', 'view_problems', 'moderate_problems', 'assign_problems', 'view_initiatives', 'view_events', 'view_reports', 'approve_reports', 'view_categories'],
                        is_system: false, users_count: 5
                    },
                    {
                        id: 5, name: 'Системный администратор', description: 'Полный доступ ко всем функциям системы',
                        permissions: ALL_PERMISSIONS.map(p => p.key),
                        is_system: true, users_count: 2
                    }
                ])
            }, 400)
        })
    }
}