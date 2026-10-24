import { ref } from 'vue'

const notification = ref(null)
let timeoutId = null

export function useNotifications() {
    function success(message, duration = 3000) {
        show({ type: 'success', message, duration })
    }

    function error(message, duration = 5000) {
        show({ type: 'error', message, duration })
    }

    function warning(message, duration = 4000) {
        show({ type: 'warning', message, duration })
    }

    function info(message, duration = 3000) {
        show({ type: 'info', message, duration })
    }

    function show({ type, message, duration }) {
        if (timeoutId) clearTimeout(timeoutId)
        notification.value = { type, message }
        timeoutId = setTimeout(() => {
            notification.value = null
        }, duration)
    }

    function clear() {
        notification.value = null
        if (timeoutId) clearTimeout(timeoutId)
    }

    return {
        notification,
        success,
        error,
        warning,
        info,
        clear
    }
}