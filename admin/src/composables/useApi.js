import { ref } from 'vue'

/**
 * Универсальный composable для работы с API
 * Автоматически управляет состоянием загрузки и ошибок
 */
export function useApi(apiFn) {
    const data = ref(null)
    const error = ref(null)
    const isLoading = ref(false)

    async function execute(...args) {
        isLoading.value = true
        error.value = null
        try {
            data.value = await apiFn(...args)
            return data.value
        } catch (e) {
            error.value = e.response?.data?.detail || e.message || 'Ошибка запроса'
            throw e
        } finally {
            isLoading.value = false
        }
    }

    function reset() {
        data.value = null
        error.value = null
        isLoading.value = false
    }

    return { data, error, isLoading, execute, reset }
}