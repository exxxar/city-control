// client/src/api/errors.js

/**
 * Извлекает читаемое сообщение об ошибке из ответа API
 * @param {Error} error - Ошибка axios
 * @returns {string} Сообщение об ошибке
 */
export function extractErrorMessage(error) {
  if (error.response) {
    // Сервер вернул ошибку
    const { status, data } = error.response

    if (data?.detail) {
      if (Array.isArray(data.detail)) {
        return data.detail.map(e => e.message || e.msg).join(', ')
      }
      if (typeof data.detail === 'string') {
        return data.detail
      }
    }

    if (data?.message) {
      return data.message
    }

    // Стандартные сообщения по коду статуса
    const statusMessages = {
      400: 'Неверный запрос',
      401: 'Требуется авторизация',
      403: 'Недостаточно прав',
      404: 'Ресурс не найден',
      409: 'Конфликт данных',
      422: 'Ошибка валидации данных',
      500: 'Внутренняя ошибка сервера'
    }

    return statusMessages[status] || `Ошибка ${status}`
  }

  if (error.request) {
    // Запрос отправлен, но нет ответа
    return 'Нет соединения с сервером. Проверьте подключение к интернету.'
  }

  // Что-то пошло не так при настройке запроса
  return error.message || 'Произошла неизвестная ошибка'
}

/**
 * Проверяет, является ли ошибка ошибкой авторизации
 * @param {Error} error
 * @returns {boolean}
 */
export function isAuthError(error) {
  return error.response?.status === 401
}

/**
 * Проверяет, является ли ошибка ошибкой валидации
 * @param {Error} error
 * @returns {boolean}
 */
export function isValidationError(error) {
  return error.response?.status === 422
}

/**
 * Показывает уведомление об ошибке (упрощённая версия)
 * @param {Error} error
 */
export function showErrorNotification(error) {
  const message = extractErrorMessage(error)
  // В реальном приложении здесь будет вызов toast-уведомления
  console.error('[API Error]', message)
  alert(message) // Временно используем alert
}