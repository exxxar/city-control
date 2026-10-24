// client/src/api/initiatives.api.js
import api from './http'

/**
 * Получить список инициатив
 * @param {Object} [params]
 * @param {number} [params.page]
 * @param {number} [params.per_page]
 * @param {string} [params.status]
 * @returns {Promise<{items: Array, total: number}>}
 */
export async function getInitiatives(params = {}) {
  const response = await api.get('/initiatives', { params })
  return response.data
}

/**
 * Получить инициативу по ID
 * @param {number|string} initiativeId
 * @returns {Promise<Object>}
 */
export async function getInitiative(initiativeId) {
  const response = await api.get(`/initiatives/${initiativeId}`)
  return response.data
}

/**
 * Создать новую инициативу
 * @param {Object} data
 * @param {string} data.title
 * @param {string} [data.description]
 * @param {number} [data.territory_id]
 * @param {number} [data.category_id]
 * @returns {Promise<Object>}
 */
export async function createInitiative(data) {
  const response = await api.post('/initiatives', data)
  return response.data
}

/**
 * Обновить инициативу
 * @param {number|string} initiativeId
 * @param {Object} updateData
 * @returns {Promise<Object>}
 */
export async function updateInitiative(initiativeId, updateData) {
  const response = await api.patch(`/initiatives/${initiativeId}`, updateData)
  return response.data
}

/**
 * Поддержать инициативу
 * @param {number|string} initiativeId
 * @returns {Promise<{message: string, total: number}>}
 */
export async function supportInitiative(initiativeId) {
  const response = await api.post(`/initiatives/${initiativeId}/support`)
  return response.data
}

/**
 * Удалить инициативу
 * @param {number|string} initiativeId
 * @returns {Promise<void>}
 */
export async function deleteInitiative(initiativeId) {
  await api.delete(`/initiatives/${initiativeId}`)
}