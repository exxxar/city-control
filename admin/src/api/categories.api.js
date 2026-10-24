// admin/src/api/categories.api.js
import http from './http'

export const categoriesApi = {
    getAll: (type = null) =>
        http.get('/categories/issue-categories', { params: type !== null ? { type } : {} }).then(r => r.data),

    create: (data) => http.post('/admin/categories', data).then(r => r.data),
    update: (id, data) => http.put(`/admin/categories/${id}`, data).then(r => r.data),
    delete: (id) => http.delete(`/admin/categories/${id}`).then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockCategories: (type = null) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const allCategories = [
                    // TYPE 0: Проблемы
                    { id: 1, name: 'Благоустройство и городская среда', description: 'Проблемы, связанные с состоянием городской инфраструктуры.', icon: '<i class="fa-solid fa-city"></i>', type: 0, variants: '["Дороги и тротуары", "Освещение", "Уборка территории"]' },
                    { id: 2, name: 'ЖКХ и коммунальные услуги', description: 'Коммунальные проблемы: вода, отопление, электричество.', icon: '<i class="fa-solid fa-house-chimney"></i>', type: 0, variants: '["Водоснабжение", "Электроснабжение", "Отопление"]' },
                    { id: 3, name: 'Транспорт и безопасность', description: 'Проблемы транспорта, парковок и дорожной безопасности.', icon: '<i class="fa-solid fa-car-side"></i>', type: 0, variants: '["Общественный транспорт", "Парковки", "Пешеходные переходы"]' },

                    // TYPE 1: Решения
                    { id: 101, name: 'Административные меры', description: 'Организационные и управленческие действия.', icon: '<i class="fa-solid fa-clipboard-check"></i>', type: 1, variants: '["Передано в профильный отдел", "Назначена проверка"]' },
                    { id: 102, name: 'Физические работы', description: 'Ремонт, устранение повреждений, уборка.', icon: '<i class="fa-solid fa-screwdriver-wrench"></i>', type: 1, variants: '["Проведён ремонт", "Устранены повреждения"]' },

                    // TYPE 2: Трудности
                    { id: 201, name: 'Организационные сложности', description: 'Проблемы координации и взаимодействия.', icon: '<i class="fa-solid fa-diagram-project"></i>', type: 2, variants: '["Отсутствие ответственного", "Несогласованность"]' },
                    { id: 202, name: 'Финансовые ограничения', description: 'Недостаток средств, превышение бюджета.', icon: '<i class="fa-solid fa-coins"></i>', type: 2, variants: '["Отсутствие финансирования", "Превышение бюджета"]' }
                ]

                let filtered = type !== null ? allCategories.filter(c => c.type === type) : allCategories

                resolve(filtered)
            }, 400)
        })
    },

    getMockHelpFormats: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    { id: 1, name: 'Разработка и организация мероприятия' },
                    { id: 2, name: 'Закупка материалов (призы, грамоты, раздаточный материал)' },
                    { id: 3, name: 'Предоставление оборудования, материалов' },
                    { id: 4, name: 'Привлечение актива партии' },
                    { id: 5, name: 'Помощь не требуется' }
                ])
            }, 400)
        })
    }
}