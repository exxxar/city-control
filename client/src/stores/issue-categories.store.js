// client/src/stores/categories.store.js
import { defineStore } from 'pinia'
import { getCategories } from '@/api/issue-categories.api'

export const useCategoriesStore = defineStore('categories', {
    state: () => ({
        items: [],
        isLoading: false,
        isLoaded: false
    }),

    actions: {
        async fetchCategories() {
            // Если данные уже загружены, не делаем лишний запрос к серверу
            if (this.isLoaded) return

            this.isLoading = true
            try {
                this.items = await getCategories()
                this.isLoaded = true
            } catch (error) {
                console.error('Failed to fetch categories:', error)
                // Если бэкенд еще не готов, можно раскомментировать строку ниже для тестов:
                // this.items = [{ id: 1, name: 'Тестовая категория', type: 0, variants: ['Вариант 1', 'Вариант 2'] }]
            } finally {
                this.isLoading = false
            }
        }
    },

    getters: {
        // Фильтруем по type, как в вашем сидере (0 = проблемы, 1 = решения, 2 = трудности)
        problems: (state) => state.items.filter(item => item.type === 0),
        solutions: (state) => state.items.filter(item => item.type === 1),
        difficulties: (state) => state.items.filter(item => item.type === 2)
    }
})