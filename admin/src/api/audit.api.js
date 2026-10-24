// admin/src/api/audit.api.js
import http from './http'

export const auditApi = {
    getLogs: (params = {}) => http.get('/admin/audit/logs', { params }).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockLogs: (params = {}) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allLogs = [
                    { id: 1, user_name: 'Администратор', action: 'user_blocked', target: 'Пользователь Сидоров П.В.', ip: '192.168.1.100', created_at: '2024-10-20T15:30:00' },
                    { id: 2, user_name: 'Модератор Петрова', action: 'problem_approved', target: 'Обращение #103', ip: '192.168.1.101', created_at: '2024-10-20T14:20:00' },
                    { id: 3, user_name: 'Администратор', action: 'category_created', target: 'Категория "Экология"', ip: '192.168.1.100', created_at: '2024-10-20T12:15:00' },
                    { id: 4, user_name: 'Модератор Иванов', action: 'report_rejected', target: 'Отчёт #5', ip: '192.168.1.102', created_at: '2024-10-20T10:45:00' },
                    { id: 5, user_name: 'Администратор', action: 'settings_updated', target: 'Настройки уведомлений', ip: '192.168.1.100', created_at: '2024-10-20T09:30:00' }
                ]

                let filtered = allLogs
                if (params.user) filtered = filtered.filter(l => l.user_name.includes(params.user))
                if (params.action) filtered = filtered.filter(l => l.action === params.action)

                resolve(filtered)
            }, 400)
        })
    }
}