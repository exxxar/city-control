// client/src/api/notifications.api.js
import api from './http'

/**
 * Получить список уведомлений текущего пользователя
 * @param {Object} [params]
 * @param {number} [params.page]
 * @param {number} [params.per_page]
 * @param {boolean} [params.unread_only]
 * @returns {Promise<{items: Array, total: number}>}
 */
export async function getNotifications(params = {}) {
  const response = await api.get('/notifications', { params })
  return response.data
}

/**
 * Пометить уведомления как прочитанные
 * @param {Array<number>} ids - Список ID уведомлений
 * @returns {Promise<void>}
 */
export async function markNotificationsAsRead(ids) {
  await api.patch('/notifications/read', { ids })
}

/**
 * Пометить все уведомления как прочитанные
 * @returns {Promise<void>}
 */
export async function markAllAsRead() {
  await api.patch('/notifications/read-all')
}

/**
 * Получить количество непрочитанных уведомлений
 * @returns {Promise<{count: number}>}
 */
export async function getUnreadCount() {
  const response = await api.get('/notifications/unread-count')
  return response.data
}

/**
 * Удалить уведомление
 * @param {number|string} notificationId
 * @returns {Promise<void>}
 */
export async function deleteNotification(notificationId) {
  await api.delete(`/notifications/${notificationId}`)
}