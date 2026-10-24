// client/src/api/auth.api.js
import api from './http'

/**
 * Вход в систему
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{access_token: string, token_type: string}>}
 */
export async function login(email, password) {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

/**
 * Регистрация нового пользователя
 * @param {Object} userData
 * @param {string} userData.email
 * @param {string} userData.password
 * @param {string} userData.full_name
 * @param {string} [userData.phone]
 * @returns {Promise<Object>} Данные пользователя
 */
export async function register(userData) {
  const response = await api.post('/auth/register', userData)
  return response.data
}

/**
 * Обновление access-токена
 * @returns {Promise<{access_token: string}>}
 */
export async function refreshToken() {
  const response = await api.post('/auth/refresh')
  return response.data
}

/**
 * Выход из системы (инвалидация токена)
 * @returns {Promise<void>}
 */
export async function logout() {
  await api.post('/auth/logout')
}