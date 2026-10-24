// admin/src/api/auth.api.js
import http from './http'

export const authApi = {
    login: (email, password) =>
        http.post('/auth/login', {
            email: email,
            password: password
        }).then(r => r.data),

    me: () => http.get('/users/me').then(r => r.data),

    logout: () => http.post('/auth/logout').then(r => r.data)
}