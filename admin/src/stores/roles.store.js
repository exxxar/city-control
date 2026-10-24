// admin/src/stores/roles.store.js
import { defineStore } from 'pinia'
import { rolesApi, ALL_PERMISSIONS } from '@/api/roles.api'

export const useRolesStore = defineStore('roles', {
    state: () => ({
        roles: [],
        isLoading: false,
        isUsingMock: false
    }),

    getters: {
        getRoleById: (state) => (id) => state.roles.find(r => r.id === id),
        systemRoles: (state) => state.roles.filter(r => r.is_system),
        customRoles: (state) => state.roles.filter(r => !r.is_system)
    },

    actions: {
        async fetchRoles() {
            this.isLoading = true
            try {
                try {
                    this.roles = await rolesApi.getAll()
                    this.isUsingMock = false
                } catch {
                    this.roles = await rolesApi.getMockRoles()
                    this.isUsingMock = true
                }
            } finally {
                this.isLoading = false
            }
        },

        async createRole(data) {
            try {
                const newRole = await rolesApi.create(data)
                this.roles.push(newRole)
                return true
            } catch (error) {
                console.error('Create role error:', error)
                throw error
            }
        },

        async updateRole(id, data) {
            try {
                const updated = await rolesApi.update(id, data)
                const index = this.roles.findIndex(r => r.id === id)
                if (index !== -1) this.roles[index] = updated
                return true
            } catch (error) {
                console.error('Update role error:', error)
                throw error
            }
        },

        async deleteRole(id) {
            try {
                await rolesApi.delete(id)
                this.roles = this.roles.filter(r => r.id !== id)
                return true
            } catch (error) {
                console.error('Delete role error:', error)
                throw error
            }
        }
    }
})

export { ALL_PERMISSIONS }