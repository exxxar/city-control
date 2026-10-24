// client/src/composables/useMap.js
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import { useMapStore } from '@/stores/map.store'

export function useMap(containerId, options = {}) {
  const mapStore = useMapStore()
  const map = ref(null)
  const markers = ref([])
  const clusters = ref([])
  const isReady = ref(false)

  const defaultOptions = {
    center: [55.4315, 37.5460], // Подольск
    zoom: 14,
    ...options
  }

  function initMap() {
    if (map.value) return

    map.value = L.map(containerId, defaultOptions)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map.value)

    mapStore.setMapInstance(map.value)
    isReady.value = true

    map.value.on('moveend', () => {
      const center = map.value.getCenter()
      mapStore.setCenter([center.lat, center.lng])
      mapStore.setZoom(map.value.getZoom())
    })
  }

  function addMarker(lat, lng, data = {}) {
    if (!map.value) return null

    const marker = L.marker([lat, lng], data.markerOptions || {})
      .addTo(map.value)
      .on('click', () => {
        mapStore.setSelectedProblem(data)
      })

    if (data.popup) {
      marker.bindPopup(data.popup)
    }

    markers.value.push({ marker, data })
    return marker
  }

  function removeMarker(marker) {
    if (!marker) return
    map.value.removeLayer(marker)
    markers.value = markers.value.filter(m => m.marker !== marker)
  }

  function clearMarkers() {
    markers.value.forEach(({ marker }) => {
      map.value.removeLayer(marker)
    })
    markers.value = []
  }

  function flyTo(lat, lng, zoom = 16) {
    if (!map.value) return
    map.value.flyTo([lat, lng], zoom)
  }

  function fitBounds(bounds) {
    if (!map.value || !bounds) return
    map.value.fitBounds(bounds)
  }

  function getUserLocationMarker(lat, lng) {
    return L.circleMarker([lat, lng], {
      radius: 10,
      fillColor: '#00A896',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    })
  }

  function destroyMap() {
    if (map.value) {
      map.value.remove()
      map.value = null
      isReady.value = false
    }
  }

  onUnmounted(() => {
    destroyMap()
  })

  return {
    map,
    markers,
    clusters,
    isReady,
    initMap,
    addMarker,
    removeMarker,
    clearMarkers,
    flyTo,
    fitBounds,
    getUserLocationMarker,
    destroyMap
  }
}