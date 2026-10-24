// admin/src/api/initiatives.api.js
import http from './http'

export const initiativesApi = {
    getAll: (params = {}) => http.get('/admin/initiatives', { params }).then(r => r.data),
    approve: (id) => http.post(`/admin/initiatives/${id}/approve`).then(r => r.data),
    reject: (id, reason) => http.post(`/admin/initiatives/${id}/reject`, { reason }).then(r => r.data),
    implement: (id) => http.post(`/admin/initiatives/${id}/implement`).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockInitiatives: (params = {}) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allInitiatives = [
                    {
                        id: 201,
                        title: 'Установка воркаут-площадки в парке',
                        author: 'Иванов И.И.',
                        category: 'Благоустройство',
                        votes_up: 145,
                        votes_down: 12,
                        status: 'pending',
                        description: 'Предлагаю установить турники и брусья в центральной части парка для занятий спортом молодежи.',
                        created_at: '2024-10-18T10:00:00'
                    },
                    {
                        id: 202,
                        title: 'Организация ярмарки выходного дня',
                        author: 'Петрова А.С.',
                        category: 'Культура, спорт и мероприятия',
                        votes_up: 89,
                        votes_down: 5,
                        status: 'approved',
                        description: 'Разрешить проведение ярмарки фермерских продуктов каждые выходные на площади.',
                        created_at: '2024-10-15T14:30:00'
                    },
                    {
                        id: 203,
                        title: 'Запрет на парковку у детской площадки',
                        author: 'Сидоров П.В.',
                        category: 'Транспорт и безопасность',
                        votes_up: 210,
                        votes_down: 45,
                        status: 'implemented',
                        description: 'Установить знаки и столбики, чтобы машины не парковались на газоне у площадки.',
                        created_at: '2024-09-20T09:15:00'
                    },
                    {
                        id: 204,
                        title: 'Создание клуба настольного тенниса',
                        author: 'Козлова М.А.',
                        category: 'Культура, спорт и мероприятия',
                        votes_up: 34,
                        votes_down: 8,
                        status: 'rejected',
                        description: 'Выделить помещение в ДК для секции тенниса.',
                        reject_reason: 'На данный момент свободных помещений в ДК нет. Рассмотрите вопрос в следующем квартале.',
                        created_at: '2024-10-10T11:20:00'
                    }
                ]

                let filtered = allInitiatives
                if (params.status) filtered = filtered.filter(i => i.status === params.status)
                if (params.search) {
                    const search = params.search.toLowerCase()
                    filtered = filtered.filter(i => i.title.toLowerCase().includes(search) || i.author.toLowerCase().includes(search))
                }

                const page = params.page || 1
                const per_page = params.per_page || 20
                const start = (page - 1) * per_page

                resolve({
                    items: filtered.slice(start, start + per_page),
                    total: filtered.length,
                    page,
                    per_page,
                    pages: Math.ceil(filtered.length / per_page)
                })
            }, 400)
        })
    }
}