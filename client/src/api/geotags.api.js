// client/src/api/geotags.api.js
import api from './http'

/**
 * Получить список гео-меток
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getGeoTags(params = {}) {
  const response = await api.get('/geotags', { params })
  return response.data
}

/**
 * Получить гео-метку по ID
 * @param {number|string} geoTagId
 * @returns {Promise<Object>}
 */
export async function getGeoTag(geoTagId) {
  const response = await api.get(`/geotags/${geoTagId}`)
  return response.data
}

/**
 * Создать гео-метку
 * @param {Object} data
 * @param {string} data.type - 'gps' | 'polygon' | 'qr' | 'indoor'
 * @param {number} [data.latitude]
 * @param {number} [data.longitude]
 * @param {number} [data.radius]
 * @param {Object} [data.geometry] - GeoJSON
 * @param {number} [data.building_id]
 * @param {number} [data.floor_id]
 * @param {number} [data.room_id]
 * @returns {Promise<Object>}
 */
export async function createGeoTag(data) {
  const response = await api.post('/geotags', data)
  return response.data
}

/**
 * Обновить гео-метку
 * @param {number|string} geoTagId
 * @param {Object} updateData
 * @returns {Promise<Object>}
 */
export async function updateGeoTag(geoTagId, updateData) {
  const response = await api.patch(`/geotags/${geoTagId}`, updateData)
  return response.data
}

/**
 * Удалить гео-метку
 * @param {number|string} geoTagId
 * @returns {Promise<void>}
 */
export async function deleteGeoTag(geoTagId) {
  await api.delete(`/geotags/${geoTagId}`)
}

/**
 * Найти ближайшие гео-метки
 * @param {number} latitude
 * @param {number} longitude
 * @param {number} [radius=1000] - Радиус в метрах
 * @returns {Promise<Array>}
 */
export async function getNearbyGeoTags(latitude, longitude, radius = 1000) {
  const response = await api.get('/geotags/nearby', {
    params: { lat: latitude, lng: longitude, radius }
  })
  return response.data
}

/**
 * Зафиксировать событие гео-метки (вход в зону, скан QR)
 * @param {number|string} geoTagId
 * @param {string} eventType - 'enter' | 'exit' | 'scan'
 * @param {Object} [metadata]
 * @returns {Promise<Object>}
 */
export async function logGeoTagEvent(geoTagId, eventType, metadata = null) {
  const response = await api.post(`/geotags/${geoTagId}/events`, {
    event_type: eventType,
    metadata
  })
  return response.data
}

/**
 * Получить гео-метку по QR-токену
 * @param {string} qrToken
 * @returns {Promise<Object>}
 */
export async function getGeoTagByQr(qrToken) {
  const response = await api.get(`/geotags/qr/${qrToken}`)
  return response.data
}