// client/src/stores/helpFormats.store.js
import { defineStore } from 'pinia'
import { getHelpFormats } from '@/api/helpFormats.api'

export const useHelpFormatsStore = defineStore('helpFormats', {
    state: () => ({
        items: [],
        isLoading: false,
        isLoaded: false
    }),

    actions: {
        async fetchHelpFormats() {
            // Если данные уже загружены, не делаем лишний запрос к серверу
            if (this.isLoaded) return

            this.isLoading = true
            try {
                this.items = await getHelpFormats()
                this.isLoaded = true
            } catch (error) {
                console.error('Failed to fetch help formats:', error)
                // Если бэкенд еще не готов, можно раскомментировать строку ниже для тестов:
                // this.items = [{ id: 1, name: 'Разработка и организация мероприятия' }, { id: 2, name: 'Помощь не требуется' }]
            } finally {
                this.isLoading = false
            }
        }
    }
})