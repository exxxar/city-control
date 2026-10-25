// client/src/api/categories.api.js
import api from './http'

/**
 * Получить список категорий (дерево)
 * @returns {Promise<Array>}
 */
export const getCategories = async (type = 0) => {
  try {
    // Если в http baseURL уже есть '/api', то путь будет '/categories'
    // Если нет, используйте '/api/categories'
    const response = await api.get(`/categories?type=${type}`)
    return response.data
  } catch (error) {
    console.error('Ошибка загрузки категорий:', error)
    throw error
  }
}


/**
 * Получить список приоритетов
 * @returns {Promise<Array>}
 */
export async function getPriorities() {
  const response = await api.get('/priorities')
  return response.data
}

/**
 * Получить список организаций-исполнителей
 * @returns {Promise<Array>}
 */
export async function getOrganizations() {
  const response = await api.get('/organizations')
  return response.data
}