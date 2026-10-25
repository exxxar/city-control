import { ref } from 'vue'

// Формула гаверсинуса для расчета расстояния в метрах между двумя координатами
function getDistanceInMeters(lat1, lon1, lat2, lon2) {
    const R = 6371e3 // Радиус Земли в метрах
    const φ1 = (lat1 * Math.PI) / 180
    const φ2 = (lat2 * Math.PI) / 180
    const Δφ = ((lat2 - lat1) * Math.PI) / 180
    const Δλ = ((lon2 - lon1) * Math.PI) / 180

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) *
        Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return R * c // Расстояние в метрах
}

export function useProximityAlert(problems, radiusMeters = 150) {
    const isWatching = ref(false)
    const watchId = ref(null)
    // Храним ID проблем, о которых уже уведомили, чтобы не спамить
    const notifiedProblemIds = ref(new Set())

    const requestNotificationPermission = async () => {
        if ('Notification' in window && Notification.permission !== 'granted') {
            const permission = await Notification.requestPermission()
            return permission === 'granted'
        }
        return true
    }

    const startWatching = async () => {
        if (!navigator.geolocation) {
            alert('Ваш браузер не поддерживает определение местоположения.')
            return
        }

        const hasPermission = await requestNotificationPermission()
        if (!hasPermission) return

        isWatching.value = true

        watchId.value = navigator.geolocation.watchPosition(
            (position) => {
                checkProximity(position.coords.latitude, position.coords.longitude)
            },
            (error) => {
                isWatching.value = false

                // === ОБРАБОТКА ОТКАЗА В ДОСТУПЕ ===
                if (error.code === error.PERMISSION_DENIED) {
                    console.warn('Пользователь запретил доступ к геолокации')
                    // Здесь можно вызвать ваш UI-компонент (например, Toast или Modal)
                    alert('Для работы оповещений необходимо разрешить доступ к геолокации в настройках браузера (значок замка в адресной строке).')
                } else if (error.code === error.POSITION_UNAVAILABLE) {
                    alert('Не удалось определить местоположение. Проверьте GPS или подключение к интернету.')
                } else if (error.code === error.TIMEOUT) {
                    alert('Превышено время ожидания ответа от спутников/GPS.')
                }
            },
            {
                enableHighAccuracy: true,
                maximumAge: 10000,
                timeout: 5000
            }
        )
    }

    const stopWatching = () => {
        if (watchId.value) {
            navigator.geolocation.clearWatch(watchId.value)
            watchId.value = null
        }
        isWatching.value = false
    }

    const checkProximity = (currentLat, currentLon) => {
        if (!problems.value || problems.value.length === 0) return

        for (const problem of problems.value) {
            // Поддерживаем как прямые поля, так и вложенный geo_tag (из вашего JSON)
            const pLat = problem.latitude || problem.geo_tag?.latitude
            const pLon = problem.longitude || problem.geo_tag?.longitude

            if (!pLat || !pLon) continue

            const distance = getDistanceInMeters(currentLat, currentLon, pLat, pLon)

            // Если мы в радиусе И еще не уведомляли об этой проблеме
            if (distance <= radiusMeters && !notifiedProblemIds.value.has(problem.id)) {
                triggerNotification(problem, distance)
                notifiedProblemIds.value.add(problem.id)
            }
        }
    }

    const triggerNotification = (problem, distance) => {
        const distanceText = distance < 1000 ? `${Math.round(distance)} м` : `${(distance / 1000).toFixed(1)} км`

        // Вариант 1: Системное уведомление браузера (работает даже если вкладка свернута)
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('📍 Проблема рядом с вами!', {
                body: `"${problem.title}" находится всего в ${distanceText}. Нажмите, чтобы посмотреть.`,
                icon: '/favicon.ico', // Замените на путь к вашему логотипу
                tag: `problem-${problem.id}`, // Группирует уведомления
                requireInteraction: true // Уведомление не исчезнет, пока пользователь не кликнет
            })
        }

        // Вариант 2: Здесь можно вызвать глобальный store для показа красивого UI-тоста внутри приложения
        // useToastStore().show({ type: 'warning', message: `Рядом: ${problem.title}` })

        console.log(`[PROXIMITY ALERT] "${problem.title}" в ${distanceText}`)
    }

    // Очистка истории уведомлений (например, при обновлении списка проблем)
    const clearNotificationHistory = () => {
        notifiedProblemIds.value.clear()
    }

    return {
        isWatching,
        startWatching,
        stopWatching,
        clearNotificationHistory
    }
}