// client/src/api/maps.api.js
import api from './http'

// === Территории ===

/**
 * Получить иерархию территорий (дерево)
 * @returns {Promise<Array>}
 */
export async function getTerritoryTree() {
  const response = await api.get('/territories/tree')
  return response.data
}

/**
 * Получить список территорий (плоский)
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getTerritories(params = {}) {
  const response = await api.get('/territories', { params })
  return response.data
}

/**
 * Создать территорию
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export async function createTerritory(data) {
  const response = await api.post('/territories', data)
  return response.data
}

// === Муниципальные объекты ===

/**
 * Получить список объектов
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getObjects(params = {}) {
  const response = await api.get('/objects', { params })
  return response.data
}

/**
 * Создать объект
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export async function createObject(data) {
  const response = await api.post('/objects', data)
  return response.data
}

// === Здания ===

/**
 * Получить список зданий
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getBuildings(params = {}) {
  const response = await api.get('/buildings', { params })
  return response.data
}

/**
 * Создать здание
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export async function createBuilding(data) {
  const response = await api.post('/buildings', data)
  return response.data
}

// === Внутренние карты ===

/**
 * Получить список слоёв внутренних карт
 * @param {Object} [params]
 * @returns {Promise<Array>}
 */
export async function getIndoorMapLayers(params = {}) {
  const response = await api.get('/indoor-maps', { params })
  return response.data
}

/**
 * Создать слой внутренней карты
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export async function createIndoorMapLayer(data) {
  const response = await api.post('/indoor-maps', data)
  return response.data
}

/**
 * Получить зоны/помещения на слое карты
 * @param {number|string} layerId
 * @returns {Promise<Array>}
 */
export async function getMapZones(layerId) {
  const response = await api.get(`/indoor-maps/${layerId}/zones`)
  return response.data
}

/**
 * Создать зону на слое карты
 * @param {number|string} layerId
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export async function createMapZone(layerId, data) {
  const response = await api.post(`/indoor-maps/${layerId}/zones`, data)
  return response.data
}