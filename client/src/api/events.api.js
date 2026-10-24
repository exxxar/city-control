// client/src/api/events.api.js
import api from './http'

/**
 * Получить список мероприятий
 * @param {Object} [params]
 * @param {number} [params.page]
 * @param {number} [params.per_page]
 * @param {string} [params.status]
 * @returns {Promise<{items: Array, total: number}>}
 */
export async function getEvents(params = {}) {
  const response = await api.get('/events', { params })
  return response.data
}

/**
 * Получить мероприятие по ID
 * @param {number|string} eventId
 * @returns {Promise<Object>}
 */
export async function getEvent(eventId) {
  const response = await api.get(`/events/${eventId}`)
  return response.data
}

/**
 * Создать заявку на мероприятие
 * @param {Object} data
 * @param {string} data.title
 * @param {string} data.event_type
 * @param {string} data.start_date - ISO datetime
 * @param {string} [data.end_date]
 * @param {string} [data.description]
 * @param {string} [data.location_text]
 * @param {number} [data.expected_participants]
 * @returns {Promise<Object>}
 */
export async function createEvent(data) {
  const response = await api.post('/events', data)
  return response.data
}

/**
 * Обновить мероприятие
 * @param {number|string} eventId
 * @param {Object} updateData
 * @returns {Promise<Object>}
 */
export async function updateEvent(eventId, updateData) {
  const response = await api.patch(`/events/${eventId}`, updateData)
  return response.data
}

/**
 * Изменить статус мероприятия (для модераторов)
 * @param {number|string} eventId
 * @param {string} newStatus
 * @returns {Promise<Object>}
 */
export async function changeEventStatus(eventId, newStatus) {
  const response = await api.patch(`/events/${eventId}/status`, { status: newStatus })
  return response.data
}

/**
 * Удалить мероприятие
 * @param {number|string} eventId
 * @returns {Promise<void>}
 */
export async function deleteEvent(eventId) {
  await api.delete(`/events/${eventId}`)
}