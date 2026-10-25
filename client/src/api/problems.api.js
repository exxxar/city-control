// client/src/api/problems.api.js
import api from './http'

/**
 * Получить список проблем с фильтрами и пагинацией
 * @param {Object} [params]
 * @param {number} [params.page]
 * @param {number} [params.per_page]
 * @param {string} [params.status]
 * @param {number} [params.category_id]
 * @param {number} [params.territory_id]
 * @returns {Promise<{items: Array, total: number, page: number, per_page: number, pages: number}>}
 */
export async function getProblems(params = {}) {
  const response = await api.get('/problems', { params })
  return response.data
}

export async function getProblemReportAsWord(id) {
  return api.get(`/problems/${id}/report.docx`, {
    responseType: 'blob'
  })
}

/**
 * Получить проблему по ID
 * @param {number|string} problemId
 * @returns {Promise<Object>}
 */
export async function getProblem(problemId) {
  const response = await api.get(`/problems/${problemId}`)
  return response.data
}

/**
 * Создать новую проблему
 * @param {Object} problemData
 * @param {string} problemData.title
 * @param {string} [problemData.description]
 * @param {number} problemData.category_id
 * @param {number} [problemData.territory_id]
 * @param {number} [problemData.geo_tag_id]
 * @param {number} [problemData.priority_id]
 * @returns {Promise<Object>}
 */
export async function createProblem(problemData) {
  const response = await api.post('/problems', problemData)
  return response.data
}

/**
 * Обновить проблему
 * @param {number|string} problemId
 * @param {Object} updateData
 * @returns {Promise<Object>}
 */
export async function updateProblem(problemId, updateData) {
  const response = await api.patch(`/problems/${problemId}`, updateData)
  return response.data
}

/**
 * Удалить проблему
 * @param {number|string} problemId
 * @returns {Promise<void>}
 */
export async function deleteProblem(problemId) {
  await api.delete(`/problems/${problemId}`)
}

/**
 * Изменить статус проблемы
 * @param {number|string} problemId
 * @param {string} newStatus
 * @param {string} [comment]
 * @returns {Promise<Object>}
 */
export async function changeProblemStatus(problemId, newStatus, comment = null) {
  const response = await api.post(`/problems/${problemId}/status`, {
    status: newStatus,
    comment
  })
  return response.data
}

/**
 * Получить историю статусов проблемы
 * @param {number|string} problemId
 * @returns {Promise<Array>}
 */
export async function getProblemHistory(problemId) {
  const response = await api.get(`/problems/${problemId}/history`)
  return response.data
}

/**
 * Подтвердить проблему (добавить факт)
 * @param {number|string} problemId
 * @returns {Promise<Object>}
 */
export async function confirmProblem(problemId) {
  const response = await api.post(`/problems/${problemId}/confirmations`)
  return response.data
}

/**
 * Получить список подтверждений проблемы
 * @param {number|string} problemId
 * @returns {Promise<Array>}
 */
export async function getProblemConfirmations(problemId) {
  const response = await api.get(`/problems/${problemId}/confirmations`)
  return response.data
}

/**
 * Подписаться на проблему
 * @param {number|string} problemId
 * @returns {Promise<void>}
 */
export async function subscribeToProblem(problemId) {
  await api.post(`/problems/${problemId}/subscribe`)
}

/**
 * Отписаться от проблемы
 * @param {number|string} problemId
 * @returns {Promise<void>}
 */
export async function unsubscribeFromProblem(problemId) {
  await api.delete(`/problems/${problemId}/subscribe`)
}

/**
 * Поиск похожих проблем (матчинг)
 * @param {Object} params
 * @param {number} [params.category_id]
 * @param {number} [params.territory_id]
 * @param {number} [params.latitude]
 * @param {number} [params.longitude]
 * @returns {Promise<Array>}
 */
export async function findSimilarProblems(params) {
  const response = await api.get('/problems/match', { params })
  return response.data
}

/**
 * Получить мои проблемы (созданные текущим пользователем)
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getMyProblems(params = {}) {
  const response = await api.get('/problems/my', { params })
  return response.data
}