// client/src/api/helpFormats.api.js
import api from '@/api/http'

export const getHelpFormats = () => {
    // Путь соответствует роуту на бэкенде: /api/help-formats/help-formats
    return api.get('/help-formats/help-formats').then(response => response.data)
}