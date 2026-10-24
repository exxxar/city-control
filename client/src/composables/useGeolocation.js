// client/src/composables/useGeolocation.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useGeolocation(options = {}) {
  const latitude = ref(null)
  const longitude = ref(null)
  const accuracy = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const isSupported = ref('geolocation' in navigator)

  let watchId = null

  const defaultOptions = {
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 0,
    ...options
  }

  async function getCurrentPosition() {
    if (!isSupported.value) {
      error.value = 'Геолокация не поддерживается браузером'
      return null
    }

    isLoading.value = true
    error.value = null

    return new Promise((resolve) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          latitude.value = position.coords.latitude
          longitude.value = position.coords.longitude
          accuracy.value = position.coords.accuracy
          isLoading.value = false
          resolve({
            latitude: latitude.value,
            longitude: longitude.value,
            accuracy: accuracy.value
          })
        },
        (err) => {
          error.value = getErrorMessage(err.code)
          isLoading.value = false
          resolve(null)
        },
        defaultOptions
      )
    })
  }

  function startWatching() {
    if (!isSupported.value || watchId !== null) return

    watchId = navigator.geolocation.watchPosition(
      (position) => {
        latitude.value = position.coords.latitude
        longitude.value = position.coords.longitude
        accuracy.value = position.coords.accuracy
        error.value = null
      },
      (err) => {
        error.value = getErrorMessage(err.code)
      },
      defaultOptions
    )
  }

  function stopWatching() {
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId)
      watchId = null
    }
  }

  function getErrorMessage(code) {
    switch (code) {
      case 1:
        return 'Доступ к геолокации запрещён. Разрешите в настройках браузера.'
      case 2:
        return 'Геолокация недоступна'
      case 3:
        return 'Превышено время ожидания'
      default:
        return 'Неизвестная ошибка геолокации'
    }
  }

  function getDistanceTo(lat2, lon2) {
    if (!latitude.value || !longitude.value) return null

    const R = 6371e3 // Радиус Земли в метрах
    const φ1 = latitude.value * Math.PI / 180
    const φ2 = lat2 * Math.PI / 180
    const Δφ = (lat2 - latitude.value) * Math.PI / 180
    const Δλ = (lon2 - longitude.value) * Math.PI / 180

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return R * c // Расстояние в метрах
  }

  onUnmounted(() => {
    stopWatching()
  })

  return {
    latitude,
    longitude,
    accuracy,
    isLoading,
    error,
    isSupported,
    getCurrentPosition,
    startWatching,
    stopWatching,
    getDistanceTo
  }
}