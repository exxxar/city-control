// admin/src/stores/settings.store.js
import { defineStore } from 'pinia'
import { settingsApi } from '@/api/settings.api'

export const useSettingsStore = defineStore('settings', {
    state: () => ({
        settings: null,
        isLoading: false,
        isUsingMock: false,
        isSaving: false
    }),

    actions: {
        async fetchSettings() {
            this.isLoading = true
            try {
                try {
                    this.settings = await settingsApi.getAll()
                    this.isUsingMock = false
                } catch {
                    this.settings = await settingsApi.getMockSettings()
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        },

        async updateSettings(data) {
            this.isSaving = true
            try {
                const updated = await settingsApi.update(data)
                this.settings = updated
                return true
            } catch (error) {
                console.error('Update settings error:', error)
                throw error
            } finally {
                this.isSaving = false
            }
        }
    }
})