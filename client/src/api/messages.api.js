// client/src/api/messages.api.js
import api from './http'

/**
 * Получить сообщения чата проблемы
 * @param {number|string} problemId
 * @param {Object} [params]
 * @param {number} [params.page]
 * @param {number} [params.per_page]
 * @returns {Promise<{items: Array, total: number}>}
 */
export async function getMessages(problemId, params = {}) {
  const response = await api.get(`/problems/${problemId}/messages`, { params })
  return response.data
}

/**
 * Отправить сообщение в чат проблемы
 * @param {number|string} problemId
 * @param {string} content - Текст сообщения
 * @returns {Promise<Object>}
 */
export async function sendMessage(problemId, content) {
  const response = await api.post(`/problems/${problemId}/messages`, { content })
  return response.data
}

/**
 * Удалить сообщение (только для автора или модератора)
 * @param {number|string} problemId
 * @param {number|string} messageId
 * @returns {Promise<void>}
 */
export async function deleteMessage(problemId, messageId) {
  await api.delete(`/problems/${problemId}/messages/${messageId}`)
}