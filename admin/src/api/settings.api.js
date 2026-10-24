// admin/src/api/settings.api.js
import http from './http'

export const settingsApi = {
    getAll: () => http.get('/admin/settings').then(r => r.data),
    update: (data) => http.put('/admin/settings', data).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockSettings: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    // Общие настройки
                    organization_name: 'Муниципальное образование "Город Подольск"',
                    organization_email: 'info@podolsk-mo.ru',
                    organization_phone: '+7 (495) 123-45-67',
                    organization_address: 'г. Подольск, ул. Ленина, д. 10',
                    support_email: 'support@city-pc.ru',

                    // Настройки модерации
                    auto_approve_trusted_users: true,
                    require_photos_for_problems: true,
                    min_description_length: 20,
                    max_photos_per_problem: 5,
                    max_photo_size_mb: 10,

                    // Настройки уведомлений
                    email_notifications_enabled: true,
                    push_notifications_enabled: false,
                    notify_on_new_problem: true,
                    notify_on_status_change: true,
                    notify_executor_on_assign: true,

                    // Лимиты
                    max_problems_per_day: 10,
                    max_initiatives_per_month: 5,
                    max_events_per_month: 3,
                    registration_requires_email_verification: true
                })
            }, 400)
        })
    }
}