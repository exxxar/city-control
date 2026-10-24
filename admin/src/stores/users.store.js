// admin/src/stores/users.store.js
import { defineStore } from 'pinia'
import { usersApi } from '@/api/users.api'

export const useUsersStore = defineStore('users', {
    state: () => ({
        users: [],
        roles: [],
        currentUser: null,
        isLoading: false,
        error: null,
        pagination: {
            page: 1,
            per_page: 20,
            pages: 0,
            total: 0
        },
        isUsingMock: false
    }),

    getters: {
        activeUsersCount: (state) => state.users.filter(u => u.is_active).length,
        blockedUsersCount: (state) => state.users.filter(u => !u.is_active).length
    },

    actions: {
        async fetchUsers(params = {}) {
            this.isLoading = true
            this.error = null
            try {
                try {
                    const response = await usersApi.getAll(params)
                    this.users = response.items || response
                    if (response.total !== undefined) {
                        this.pagination = {
                            page: response.page || 1,
                            per_page: response.per_page || 20,
                            pages: response.pages || 0,
                            total: response.total || 0
                        }
                    }
                    this.isUsingMock = false
                } catch {
                    const response = await usersApi.getMockUsers(params)
                    this.users = response.items || response
                    this.pagination = {
                        page: response.page || 1,
                        per_page: response.per_page || 20,
                        pages: response.pages || 0,
                        total: response.total || 0
                    }
                    this.isUsingMock = true
                }
            } catch (error) {
                this.error = error.response?.data?.detail || 'Ошибка загрузки пользователей'
                console.error('Fetch users error:', error)
            } finally {
                this.isLoading = false
            }
        },

        async fetchRoles() {
            try {
                this.roles = await usersApi.getMockRoles()
            } catch (error) {
                console.error('Fetch roles error:', error)
            }
        },

        async blockUser(id) {
            try {
                await usersApi.block(id)
                const user = this.users.find(u => u.id === id)
                if (user) user.is_active = false
                return true
            } catch (error) {
                console.error('Block user error:', error)
                throw error
            }
        },

        async unblockUser(id) {
            try {
                await usersApi.unblock(id)
                const user = this.users.find(u => u.id === id)
                if (user) user.is_active = true
                return true
            } catch (error) {
                console.error('Unblock user error:', error)
                throw error
            }
        },

        async changeRole(userId, roleId) {
            try {
                await usersApi.changeRole(userId, roleId)
                const user = this.users.find(u => u.id === userId)
                if (user) {
                    const newRole = this.roles.find(r => r.id === roleId)
                    if (newRole) user.roles = [newRole]
                }
                return true
            } catch (error) {
                console.error('Change role error:', error)
                throw error
            }
        }
    }
})