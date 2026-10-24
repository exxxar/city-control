// admin/src/api/executors.api.js
import http from './http'

export const executorsApi = {
    getStats: () => http.get('/admin/executors/stats').then(r => r.data),

    // === ВРЕМЕННЫЕ ЗАГЛУШКИ ===
    getMockStats: () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    {
                        id: 4,
                        full_name: 'Козлова Мария Александровна',
                        department: 'ЖКХ',
                        total_assigned: 45,
                        completed: 38,
                        in_progress: 5,
                        overdue: 2,
                        avg_resolution_time: 3.2,
                        rating: 4.8,
                        last_activity: '2024-10-20T14:30:00'
                    },
                    {
                        id: 8,
                        full_name: 'Федорова Ольга Игоревна',
                        department: 'Дороги',
                        total_assigned: 32,
                        completed: 28,
                        in_progress: 3,
                        overdue: 1,
                        avg_resolution_time: 4.5,
                        rating: 4.6,
                        last_activity: '2024-10-20T11:20:00'
                    },
                    {
                        id: 15,
                        full_name: 'Смирнов Виктор Олегович',
                        department: 'Благоустройство',
                        total_assigned: 28,
                        completed: 25,
                        in_progress: 2,
                        overdue: 1,
                        avg_resolution_time: 2.8,
                        rating: 4.9,
                        last_activity: '2024-10-20T15:45:00'
                    },
                    {
                        id: 22,
                        full_name: 'Морозов Дмитрий Константинович',
                        department: 'Экология',
                        total_assigned: 18,
                        completed: 15,
                        in_progress: 2,
                        overdue: 1,
                        avg_resolution_time: 5.1,
                        rating: 4.3,
                        last_activity: '2024-10-19T16:10:00'
                    },
                    {
                        id: 31,
                        full_name: 'Волкова Елена Николаевна',
                        department: 'Транспорт',
                        total_assigned: 24,
                        completed: 20,
                        in_progress: 3,
                        overdue: 1,
                        avg_resolution_time: 3.8,
                        rating: 4.5,
                        last_activity: '2024-10-20T09:30:00'
                    }
                ])
            }, 500)
        })
    }
}