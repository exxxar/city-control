// admin/src/composables/useTheme.js
import { ref, watch } from 'vue'

const isDark = ref(localStorage.getItem('admin_theme') === 'dark')

export function useTheme() {
    function toggleTheme() {
        isDark.value = !isDark.value
        localStorage.setItem('admin_theme', isDark.value ? 'dark' : 'light')
        applyTheme()
    }

    function applyTheme() {
        if (isDark.value) {
            document.documentElement.classList.add('dark-theme')
        } else {
            document.documentElement.classList.remove('dark-theme')
        }
    }

    watch(isDark, applyTheme, { immediate: true })

    return { isDark, toggleTheme }
}