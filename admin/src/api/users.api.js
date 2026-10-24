// admin/src/api/users.api.js
import http from './http'

export const usersApi = {
    getAll: (params = {}) =>
        http.get('/admin/users', { params }).then(r => r.data),

    getById: (id) => http.get(`/admin/users/${id}`).then(r => r.data),

    update: (id, data) =>
        http.put(`/admin/users/${id}`, data).then(r => r.data),

    block: (id) => http.post(`/admin/users/${id}/block`).then(r => r.data),

    unblock: (id) => http.post(`/admin/users/${id}/unblock`).then(r => r.data),

    changeRole: (id, roleId) =>
        http.post(`/admin/users/${id}/role`, { role_id: roleId }).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockUsers: (params = {}) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allUsers = [
                    { id: 1, full_name: 'Иванов Иван Иванович', email: 'ivanov@mail.ru', phone: '+7 (999) 123-45-67', roles: [{ id: 1, name: 'Пользователь' }], is_active: true, created_at: '2024-01-15T10:30:00', last_login: '2024-10-20T14:20:00' },
                    { id: 2, full_name: 'Петрова Анна Сергеевна', email: 'petrova@gmail.com', phone: '+7 (999) 234-56-78', roles: [{ id: 2, name: 'Модератор' }], is_active: true, created_at: '2024-02-20T09:15:00', last_login: '2024-10-20T11:45:00' },
                    { id: 3, full_name: 'Сидоров Петр Владимирович', email: 'sidorov@yandex.ru', phone: '+7 (999) 345-67-89', roles: [{ id: 1, name: 'Пользователь' }], is_active: false, created_at: '2024-03-10T14:20:00', last_login: '2024-09-15T16:30:00' },
                    { id: 4, full_name: 'Козлова Мария Александровна', email: 'kozlova@mail.ru', phone: '+7 (999) 456-78-90', roles: [{ id: 3, name: 'Исполнитель' }], is_active: true, created_at: '2024-04-05T11:10:00', last_login: '2024-10-19T09:20:00' },
                    { id: 5, full_name: 'Морозов Дмитрий Константинович', email: 'morozov@gmail.com', phone: '+7 (999) 567-89-01', roles: [{ id: 1, name: 'Пользователь' }], is_active: true, created_at: '2024-05-12T16:45:00', last_login: '2024-10-20T10:15:00' },
                    { id: 6, full_name: 'Волкова Елена Николаевна', email: 'volkova@yandex.ru', phone: '+7 (999) 678-90-12', roles: [{ id: 4, name: 'Руководитель органа' }], is_active: true, created_at: '2024-06-18T08:30:00', last_login: '2024-10-20T13:50:00' },
                    { id: 7, full_name: 'Новиков Алексей Петрович', email: 'novikov@mail.ru', phone: '+7 (999) 789-01-23', roles: [{ id: 1, name: 'Пользователь' }], is_active: true, created_at: '2024-07-22T13:25:00', last_login: '2024-10-18T17:40:00' },
                    { id: 8, full_name: 'Федорова Ольга Игоревна', email: 'fedorova@gmail.com', phone: '+7 (999) 890-12-34', roles: [{ id: 3, name: 'Исполнитель' }], is_active: false, created_at: '2024-08-30T10:50:00', last_login: '2024-09-28T12:10:00' },
                    { id: 9, full_name: 'Системный Администратор', email: 'admin@city.local', phone: '+7 (999) 000-00-00', roles: [{ id: 5, name: 'Системный администратор' }], is_active: true, created_at: '2024-01-01T00:00:00', last_login: '2024-10-20T15:00:00' },
                    { id: 10, full_name: 'Смирнов Виктор Олегович', email: 'smirnov@yandex.ru', phone: '+7 (999) 111-22-33', roles: [{ id: 1, name: 'Пользователь' }], is_active: true, created_at: '2024-09-14T15:35:00', last_login: '2024-10-19T14:25:00' },
                    { id: 11, full_name: 'Кузнецова Татьяна Михайловна', email: 'kuznetsova@mail.ru', phone: '+7 (999) 222-33-44', roles: [{ id: 1, name: 'Пользователь' }], is_active: true, created_at: '2024-10-01T09:40:00', last_login: '2024-10-20T08:55:00' },
                    { id: 12, full_name: 'Попов Сергей Андреевич', email: 'popov@gmail.com', phone: '+7 (999) 333-44-55', roles: [{ id: 2, name: 'Модератор' }], is_active: true, created_at: '2024-10-05T11:20:00', last_login: '2024-10-20T12:30:00' }
                ]

                // Фильтрация
                let filtered = allUsers

                if (params.search) {
                    const search = params.search.toLowerCase()
                    filtered = filtered.filter(u =>
                        u.full_name.toLowerCase().includes(search) ||
                        u.email.toLowerCase().includes(search) ||
                        u.phone.includes(search)
                    )
                }

                if (params.role) {
                    filtered = filtered.filter(u =>
                        u.roles.some(r => r.id === parseInt(params.role))
                    )
                }

                if (params.status === 'active') {
                    filtered = filtered.filter(u => u.is_active)
                } else if (params.status === 'blocked') {
                    filtered = filtered.filter(u => !u.is_active)
                }

                // Пагинация
                const page = params.page || 1
                const per_page = params.per_page || 20
                const start = (page - 1) * per_page
                const end = start + per_page
                const paginated = filtered.slice(start, end)

                resolve({
                    items: paginated,
                    total: filtered.length,
                    page: page,
                    per_page: per_page,
                    pages: Math.ceil(filtered.length / per_page)
                })
            }, 500)
        })
    },

    getMockRoles: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    { id: 1, name: 'Пользователь' },
                    { id: 2, name: 'Модератор' },
                    { id: 3, name: 'Исполнитель' },
                    { id: 4, name: 'Руководитель органа' },
                    { id: 5, name: 'Системный администратор' }
                ])
            }, 300)
        })
    }
}