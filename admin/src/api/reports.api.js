// admin/src/api/reports.api.js
import http from './http'

export const reportsApi = {
    getAll: (params = {}) => http.get('/admin/reports', { params }).then(r => r.data),
    getById: (id) => http.get(`/admin/reports/${id}`).then(r => r.data),
    approve: (id) => http.post(`/admin/reports/${id}/approve`).then(r => r.data),
    reject: (id, reason) => http.post(`/admin/reports/${id}/reject`, { reason }).then(r => r.data),
    requestRevision: (id, comment) => http.post(`/admin/reports/${id}/revision`, { comment }).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockReports: (params = {}) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allReports = [
                    {
                        id: 1,
                        problem_id: 103,
                        problem_title: 'Мусорный бак переполнен',
                        executor_name: 'Козлова Мария Александровна',
                        status: 'pending',
                        submitted_at: '2024-10-20T14:30:00',
                        work_description: 'Выполнен вывоз мусора, заменён повреждённый контейнер на новый. Проведена уборка прилегающей территории.',
                        work_date: '2024-10-19',
                        photos_before: 2,
                        photos_after: 3,
                        materials_used: 'Контейнер для мусора 1100л — 1 шт.',
                        cost: 15000
                    },
                    {
                        id: 2,
                        problem_id: 104,
                        problem_title: 'Сломанная лавочка',
                        executor_name: 'Смирнов Виктор Олегович',
                        status: 'approved',
                        submitted_at: '2024-10-18T11:20:00',
                        work_description: 'Произведён ремонт лавочки: заменены сломанные доски сиденья и спинки, укреплены металлические опоры, нанесено защитное покрытие.',
                        work_date: '2024-10-17',
                        photos_before: 1,
                        photos_after: 2,
                        materials_used: 'Доска обрезная 40х150 — 3 шт., Лак для дерева — 0.5л',
                        cost: 3500
                    },
                    {
                        id: 3,
                        problem_id: 107,
                        problem_title: 'Шумная стройка ночью',
                        executor_name: 'Федорова Ольга Игоревна',
                        status: 'rejected',
                        submitted_at: '2024-10-19T16:45:00',
                        work_description: 'Проведена проверка строительной площадки.',
                        work_date: '2024-10-19',
                        photos_before: 0,
                        photos_after: 0,
                        materials_used: '',
                        cost: 0,
                        reject_reason: 'Не предоставлены фото-подтверждения выполненных работ. Описание слишком краткое.'
                    },
                    {
                        id: 4,
                        problem_id: 102,
                        problem_title: 'Не горит фонарь уже неделю',
                        executor_name: 'Козлова Мария Александровна',
                        status: 'revision',
                        submitted_at: '2024-10-20T09:15:00',
                        work_description: 'Заменена лампа в фонаре освещения.',
                        work_date: '2024-10-19',
                        photos_before: 1,
                        photos_after: 1,
                        materials_used: 'Лампа светодиодная 50Вт — 1 шт.',
                        cost: 1200,
                        revision_comment: 'Необходимо указать точное время выполнения работ и предоставить фото фонаря в ночное время для подтверждения его работоспособности.'
                    },
                    {
                        id: 5,
                        problem_id: 108,
                        problem_title: 'Детская горка ржавая',
                        executor_name: 'Смирнов Виктор Олегович',
                        status: 'pending',
                        submitted_at: '2024-10-20T15:00:00',
                        work_description: 'Выполнена зачистка ржавчины, нанесено антикоррозийное покрытие, произведена окраска горки в яркие цвета. Проверена безопасность всех креплений.',
                        work_date: '2024-10-20',
                        photos_before: 3,
                        photos_after: 4,
                        materials_used: 'Грунтовка антикоррозийная — 2л, Краска эмалевая — 3л, Наждачная бумага — 5 листов',
                        cost: 4800
                    }
                ]

                let filtered = allReports

                if (params.status) {
                    filtered = filtered.filter(r => r.status === params.status)
                }

                if (params.search) {
                    const search = params.search.toLowerCase()
                    filtered = filtered.filter(r =>
                        r.problem_title.toLowerCase().includes(search) ||
                        r.executor_name.toLowerCase().includes(search)
                    )
                }

                const page = params.page || 1
                const per_page = params.per_page || 20
                const start = (page - 1) * per_page
                const paginated = filtered.slice(start, start + per_page)

                resolve({
                    items: paginated,
                    total: filtered.length,
                    page,
                    per_page,
                    pages: Math.ceil(filtered.length / per_page)
                })
            }, 500)
        })
    }
}