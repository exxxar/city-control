// client/src/composables/useGeoTags.js
import { ref, computed } from 'vue'
import * as geotagsApi from '@/api/geotags.api'

export function useGeoTags() {
  const geoTags = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const activeGeoTags = computed(() => {
    return geoTags.value.filter(tag => tag.active)
  })

  const gpsTags = computed(() => {
    return activeGeoTags.value.filter(tag => tag.type === 'gps')
  })

  const qrTags = computed(() => {
    return activeGeoTags.value.filter(tag => tag.type === 'qr')
  })

  const polygonTags = computed(() => {
    return activeGeoTags.value.filter(tag => tag.type === 'polygon')
  })

  async function fetchGeoTags(params = {}) {
    isLoading.value = true
    error.value = null
    try {
      const response = await geotagsApi.getGeoTags(params)
      geoTags.value = response
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки гео-меток'
      console.error('Failed to fetch geo tags:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchNearbyGeoTags(latitude, longitude, radius = 1000) {
    isLoading.value = true
    error.value = null
    try {
      const response = await geotagsApi.getNearbyGeoTags(latitude, longitude, radius)
      geoTags.value = response
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка загрузки ближайших меток'
      console.error('Failed to fetch nearby geo tags:', err)
    } finally {
      isLoading.value = false
    }
  }

  async function createGeoTag(data) {
    isLoading.value = true
    error.value = null
    try {
      const response = await geotagsApi.createGeoTag(data)
      geoTags.value.push(response)
      return response
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка создания гео-метки'
      console.error('Failed to create geo tag:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logGeoTagEvent(geoTagId, eventType, metadata = null) {
    try {
      await geotagsApi.logGeoTagEvent(geoTagId, eventType, metadata)
    } catch (err) {
      console.error('Failed to log geo tag event:', err)
    }
  }

  function filterByType(type) {
    return activeGeoTags.value.filter(tag => tag.type === type)
  }

  function filterByBuilding(buildingId) {
    return activeGeoTags.value.filter(tag => tag.building_id === buildingId)
  }

  return {
    geoTags,
    activeGeoTags,
    gpsTags,
    qrTags,
    polygonTags,
    isLoading,
    error,
    fetchGeoTags,
    fetchNearbyGeoTags,
    createGeoTag,
    logGeoTagEvent,
    filterByType,
    filterByBuilding
  }
}