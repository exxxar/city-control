// client/src/api/categories.api.js
import api from './http'

/**
 * Получить список категорий (дерево)
 * @returns {Promise<Array>}
 */
export async function getCategories() {
  const response = await api.get('/categories')
  return response.data
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