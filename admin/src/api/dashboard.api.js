// admin/src/api/dashboard.api.js
import http from './http'

export const dashboardApi = {
    getStats: () => http.get('/admin/dashboard/stats').then(r => r.data),

    getRecentProblems: (limit = 10) =>
        http.get('/admin/dashboard/recent-problems', { params: { limit } }).then(r => r.data),

    getCharts: () => http.get('/admin/dashboard/charts').then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ (пока нет API на бэкенде) ===
    getMockStats: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    totalUsers: 1247,
                    totalProblems: 892,
                    newProblems: 47,
                    inProgressProblems: 128,
                    resolvedProblems: 717,
                    totalInitiatives: 156,
                    totalEvents: 43,
                    todayNewProblems: 12,
                    weekNewProblems: 89
                })
            }, 500)
        })
    },

    getMockRecentProblems: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    { id: 1, title: 'Яма на ул. Ленина', category: 'Дороги', status: 'new', address: 'ул. Ленина, 15', created_at: '2024-10-20T10:30:00', author: 'Иванов И.И.' },
                    { id: 2, title: 'Не горит фонарь', category: 'ЖКХ', status: 'in_progress', address: 'Парк культуры', created_at: '2024-10-20T09:15:00', author: 'Петрова А.С.' },
                    { id: 3, title: 'Мусор во дворе', category: 'Экология', status: 'new', address: 'ул. Пушкина, 5', created_at: '2024-10-20T08:45:00', author: 'Сидоров П.В.' },
                    { id: 4, title: 'Сломанная лавочка', category: 'Благоустройство', status: 'resolved', address: 'Центральный парк', created_at: '2024-10-19T16:20:00', author: 'Козлова М.А.' },
                    { id: 5, title: 'Прорыв трубы', category: 'ЖКХ', status: 'in_progress', address: 'ул. Гагарина, 22', created_at: '2024-10-19T14:10:00', author: 'Морозов Д.К.' },
                    { id: 6, title: 'Отсутствует знак', category: 'Транспорт', status: 'new', address: 'ул. Советская, 8', created_at: '2024-10-19T11:30:00', author: 'Волкова Е.Н.' }
                ])
            }, 500)
        })
    }
}