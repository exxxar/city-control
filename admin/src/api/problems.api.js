// admin/src/api/problems.api.js
import http from './http'

export const problemsApi = {
    getAll: (params = {}) => http.get('/admin/problems', { params }).then(r => r.data),
    getById: (id) => http.get(`/admin/problems/${id}`).then(r => r.data),
    moderate: (id, data) => http.post(`/admin/problems/${id}/moderate`, data).then(r => r.data),
    assign: (id, executorId) => http.post(`/admin/problems/${id}/assign`, { executor_id: executorId }).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockProblems: (params = {}) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allProblems = [
                    { id: 101, title: 'Огромная яма на проезжей части', description: 'Яма глубиной около 15 см, опасно для машин.', category: 'Дороги и тротуары', address: 'ул. Ленина, д. 15, у подъезда 2', author: 'Иванов И.И.', phone: '+7 (999) 123-45-67', status: 'new', created_at: '2024-10-20T10:30:00', photos_count: 2 },
                    { id: 102, title: 'Не горит фонарь уже неделю', description: 'Темно, страшно ходить вечером.', category: 'Освещение', address: 'Парк культуры, центральная аллея', author: 'Петрова А.С.', phone: '+7 (999) 234-56-78', status: 'approved', created_at: '2024-10-19T09:15:00', photos_count: 1 },
                    { id: 103, title: 'Мусорный бак переполнен', description: 'Мусор разбросан вокруг, неприятный запах.', category: 'Уборка территории', address: 'ул. Пушкина, д. 5, во дворе', author: 'Сидоров П.В.', phone: '+7 (999) 345-67-89', status: 'in_progress', created_at: '2024-10-18T08:45:00', photos_count: 3 },
                    { id: 104, title: 'Сломанная лавочка', description: 'Спинка оторвана, сидеть невозможно.', category: 'Детские и спортивные площадки', address: 'Центральный парк, у пруда', author: 'Козлова М.А.', phone: '+7 (999) 456-78-90', status: 'resolved', created_at: '2024-10-15T16:20:00', photos_count: 1 },
                    { id: 105, title: 'Прорыв трубы, течет вода', description: 'Затапливает подвал.', category: 'Водоснабжение и канализация', address: 'ул. Гагарина, д. 22', author: 'Морозов Д.К.', phone: '+7 (999) 567-89-01', status: 'rejected', created_at: '2024-10-14T14:10:00', photos_count: 0, reject_reason: 'Не указан точный адрес, фото не загружены' },
                    { id: 106, title: 'Отсутствует дорожный знак', description: 'Снесли во время бури.', category: 'Опасные участки дорог', address: 'ул. Советская, д. 8, перекресток', author: 'Волкова Е.Н.', phone: '+7 (999) 678-90-12', status: 'new', created_at: '2024-10-20T11:30:00', photos_count: 1 },
                    { id: 107, title: 'Шумная стройка ночью', description: 'Работают после 23:00.', category: 'Шум и загрязнение', address: 'ул. Строителей, д. 1', author: 'Новиков А.П.', phone: '+7 (999) 789-01-23', status: 'in_progress', created_at: '2024-10-19T23:45:00', photos_count: 0 },
                    { id: 108, title: 'Детская горка ржавая', description: 'Ребенок поранился.', category: 'Детские и спортивные площадки', address: 'ул. Мира, д. 10, двор', author: 'Федорова О.И.', phone: '+7 (999) 890-12-34', status: 'approved', created_at: '2024-10-20T08:00:00', photos_count: 2 },
                ]

                let filtered = allProblems

                if (params.search) {
                    const search = params.search.toLowerCase()
                    filtered = filtered.filter(p =>
                        p.title.toLowerCase().includes(search) ||
                        p.address.toLowerCase().includes(search) ||
                        p.author.toLowerCase().includes(search)
                    )
                }

                if (params.status) {
                    filtered = filtered.filter(p => p.status === params.status)
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
    },

    getMockExecutors: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    { id: 4, full_name: 'Козлова Мария Александровна (ЖКХ)' },
                    { id: 8, full_name: 'Федорова Ольга Игоревна (Дороги)' },
                    { id: 15, full_name: 'Смирнов Виктор Олегович (Благоустройство)' }
                ])
            }, 300)
        })
    }
}