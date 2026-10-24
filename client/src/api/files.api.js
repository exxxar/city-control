// client/src/api/files.api.js
import api from './http'

/**
 * Загрузить файл (фото, видео, документ)
 * @param {File} file - Файл для загрузки
 * @param {string} entityType - Тип сущности ('problem', 'initiative', 'message')
 * @param {number|string} entityId - ID сущности
 * @param {Function} [onProgress] - Callback для отслеживания прогресса
 * @returns {Promise<Object>}
 */
export async function uploadFile(file, entityType, entityId, onProgress = null) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('linked_entity_type', entityType)
  formData.append('linked_entity_id', entityId)

  const response = await api.post('/attachments', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentCompleted)
      }
    }
  })
  return response.data
}

/**
 * Получить список вложений для сущности
 * @param {string} entityType
 * @param {number|string} entityId
 * @returns {Promise<Array>}
 */
export async function getAttachments(entityType, entityId) {
  const response = await api.get('/attachments', {
    params: { entity_type: entityType, entity_id: entityId }
  })
  return response.data
}

/**
 * Удалить вложение
 * @param {number|string} attachmentId
 * @returns {Promise<void>}
 */
export async function deleteAttachment(attachmentId) {
  await api.delete(`/attachments/${attachmentId}`)
}

/**
 * Сгенерировать DOCX-документ для проблемы
 * @param {number|string} problemId
 * @returns {Promise<Object>}
 */
export async function generateProblemDocx(problemId) {
  const response = await api.post('/documents/generate', { problem_id: problemId })
  return response.data
}

/**
 * Получить список документов для проблемы
 * @param {number|string} problemId
 * @returns {Promise<Array>}
 */
export async function getProblemDocuments(problemId) {
  const response = await api.get('/documents', {
    params: { problem_id: problemId }
  })
  return response.data
}

/**
 * Скачать документ (возвращает URL)
 * @param {number|string} documentId
 * @returns {Promise<{url: string}>}
 */
export async function downloadDocument(documentId) {
  const response = await api.get(`/documents/${documentId}/download`)
  return response.data
}