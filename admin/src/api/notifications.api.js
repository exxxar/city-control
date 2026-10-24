// admin/src/api/notifications.api.js
import http from './http'

export const notificationsApi = {
    getAll: () => http.get('/admin/notifications').then(r => r.data),
    markAsRead: (id) => http.post(`/admin/notifications/${id}/read`).then(r => r.data),
    markAllAsRead: () => http.post('/admin/notifications/read-all').then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockNotifications: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    {
                        id: 1,
                        type: 'new_problem',
                        title: 'Новое обращение',
                        message: 'Иванов И.И. сообщил о яме на ул. Ленина',
                        icon: 'fa-triangle-exclamation',
                        color: '#c64752',
                        created_at: '2024-10-20T15:30:00',
                        is_read: false,
                        link: '/problems'
                    },
                    {
                        id: 2,
                        type: 'report_submitted',
                        title: 'Отчёт исполнителя',
                        message: 'Козлова М.А. отправила отчёт по обращению #103',
                        icon: 'fa-file-lines',
                        color: '#0dcaf0',
                        created_at: '2024-10-20T14:20:00',
                        is_read: false,
                        link: '/reports'
                    },
                    {
                        id: 3,
                        type: 'initiative_vote',
                        title: 'Инициатива набрала голоса',
                        message: 'Инициатива "Воркаут-площадка" набрала 100+ голосов',
                        icon: 'fa-lightbulb',
                        color: '#fbbf24',
                        created_at: '2024-10-20T12:15:00',
                        is_read: true,
                        link: '/initiatives'
                    },
                    {
                        id: 4,
                        type: 'user_registered',
                        title: 'Новый пользователь',
                        message: 'Зарегистрирован новый пользователь: Петров П.П.',
                        icon: 'fa-user-plus',
                        color: '#06d6a0',
                        created_at: '2024-10-20T10:45:00',
                        is_read: true,
                        link: '/users'
                    }
                ])
            }, 400)
        })
    }
}