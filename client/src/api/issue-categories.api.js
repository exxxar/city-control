// client/src/api/categories.api.js
import api from '@/api/http'

export const getCategories = (type = null) => {
    const params = type !== null ? { type } : {}
    // Путь соответствует роуту на бэкенде: /api/categories/issue-categories
    return api.get('/categories/issue-categories', { params }).then(response => response.data)
}