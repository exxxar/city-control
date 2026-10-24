// admin/src/stores/categories.store.js
import { defineStore } from 'pinia'
import { categoriesApi } from '@/api/categories.api'

export const useCategoriesStore = defineStore('categories', {
    state: () => ({
        categories: [],
        helpFormats: [],
        isLoading: false,
        isUsingMock: false
    }),

    getters: {
        problems: (state) => state.categories.filter(c => c.type === 0),
        solutions: (state) => state.categories.filter(c => c.type === 1),
        difficulties: (state) => state.categories.filter(c => c.type === 2)
    },

    actions: {
        async fetchCategories(type = null) {
            this.isLoading = true
            try {
                try {
                    this.categories = await categoriesApi.getAll(type)
                    this.isUsingMock = false
                } catch {
                    this.categories = await categoriesApi.getMockCategories(type)
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        },

        async fetchHelpFormats() {
            try {
                this.helpFormats = await categoriesApi.getMockHelpFormats()
            } catch (error) {
                console.error('Fetch help formats error:', error)
            }
        },

        async createCategory(data) {
            try {
                const newCat = await categoriesApi.create(data)
                this.categories.push(newCat)
                return true
            } catch (error) {
                console.error('Create category error:', error)
                throw error
            }
        },

        async updateCategory(id, data) {
            try {
                const updated = await categoriesApi.update(id, data)
                const index = this.categories.findIndex(c => c.id === id)
                if (index !== -1) this.categories[index] = updated
                return true
            } catch (error) {
                console.error('Update category error:', error)
                throw error
            }
        },

        async deleteCategory(id) {
            try {
                await categoriesApi.delete(id)
                this.categories = this.categories.filter(c => c.id !== id)
                return true
            } catch (error) {
                console.error('Delete category error:', error)
                throw error
            }
        }
    }
})