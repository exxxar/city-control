// client/src/composables/useMediaUpload.js
import { ref } from 'vue'
import * as filesApi from '@/api/files.api'

export function useMediaUpload(options = {}) {
  const files = ref([])
  const isUploading = ref(false)
  const uploadProgress = ref(0)
  const error = ref(null)

  const defaultOptions = {
    maxFileSize: 10 * 1024 * 1024, // 10 MB
    allowedTypes: ['image/jpeg', 'image/png', 'image/webp', 'video/mp4'],
    maxFiles: 10,
    ...options
  }

  function validateFile(file) {
    if (file.size > defaultOptions.maxFileSize) {
      return `Файл "${file.name}" превышает ${defaultOptions.maxFileSize / 1024 / 1024} МБ`
    }

    if (!defaultOptions.allowedTypes.includes(file.type)) {
      return `Файл "${file.name}" имеет недопустимый тип`
    }

    if (files.value.length >= defaultOptions.maxFiles) {
      return `Максимум ${defaultOptions.maxFiles} файлов`
    }

    return null
  }

  function addFiles(fileList) {
    error.value = null

    for (const file of fileList) {
      const validationError = validateFile(file)
      if (validationError) {
        error.value = validationError
        return false
      }

      const preview = file.type.startsWith('image/')
        ? URL.createObjectURL(file)
        : null

      files.value.push({
        file,
        preview,
        name: file.name,
        size: file.size,
        type: file.type,
        progress: 0,
        uploaded: false,
        attachmentId: null
      })
    }

    return true
  }

  function removeFile(index) {
    const fileObj = files.value[index]
    if (fileObj.preview) {
      URL.revokeObjectURL(fileObj.preview)
    }
    files.value.splice(index, 1)
  }

  async function uploadFiles(entityType, entityId) {
    isUploading.value = true
    error.value = null

    const results = []

    for (let i = 0; i < files.value.length; i++) {
      const fileObj = files.value[i]
      if (fileObj.uploaded) continue

      try {
        const response = await filesApi.uploadFile(
          fileObj.file,
          entityType,
          entityId,
          (progress) => {
            fileObj.progress = progress
            uploadProgress.value = Math.round(
              files.value.reduce((sum, f) => sum + f.progress, 0) / files.value.length
            )
          }
        )

        fileObj.uploaded = true
        fileObj.attachmentId = response.id
        results.push(response)
      } catch (err) {
        error.value = `Ошибка загрузки "${fileObj.name}": ${err.response?.data?.detail || err.message}`
        console.error('Upload failed:', err)
      }
    }

    isUploading.value = false
    uploadProgress.value = 0

    return results
  }

  function clearFiles() {
    files.value.forEach(f => {
      if (f.preview) URL.revokeObjectURL(f.preview)
    })
    files.value = []
    uploadProgress.value = 0
  }

  return {
    files,
    isUploading,
    uploadProgress,
    error,
    addFiles,
    removeFile,
    uploadFiles,
    clearFiles,
    validateFile
  }
}