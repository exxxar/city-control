// client/src/stores/map.store.js
import { defineStore } from 'pinia'

export const useMapStore = defineStore('map', {
  state: () => ({
    center: [55.4315, 37.5460], // Подольск по умолчанию
    zoom: 14,
    userLocation: null,
    selectedProblem: null,
    markers: [],
    clusters: [],
    filters: {
      status: null,
      category: null,
      priority: null,
      dateRange: null
    },
    showUserLocation: false,
    mapInstance: null,
    isLoading: false
  }),

  getters: {
    filteredMarkers: (state) => {
      let filtered = state.markers

      if (state.filters.status) {
        filtered = filtered.filter(m => m.status === state.filters.status)
      }

      if (state.filters.category) {
        filtered = filtered.filter(m => m.category_id === state.filters.category)
      }

      if (state.filters.priority) {
        filtered = filtered.filter(m => m.priority_id === state.filters.priority)
      }

      return filtered
    },

    hasActiveFilters: (state) => {
      return state.filters.status || state.filters.category || state.filters.priority
    }
  },

  actions: {
    setCenter(center) {
      this.center = center
    },

    setZoom(zoom) {
      this.zoom = zoom
    },

    setUserLocation(location) {
      this.userLocation = location
    },

    setSelectedProblem(problem) {
      this.selectedProblem = problem
    },

    clearSelectedProblem() {
      this.selectedProblem = null
    },

    setMarkers(markers) {
      this.markers = markers
    },

    addMarker(marker) {
      this.markers.push(marker)
    },

    removeMarker(markerId) {
      this.markers = this.markers.filter(m => m.id !== markerId)
    },

    updateMarker(markerId, updates) {
      const index = this.markers.findIndex(m => m.id === markerId)
      if (index !== -1) {
        this.markers[index] = { ...this.markers[index], ...updates }
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    resetFilters() {
      this.filters = {
        status: null,
        category: null,
        priority: null,
        dateRange: null
      }
    },

    toggleUserLocation() {
      this.showUserLocation = !this.showUserLocation
    },

    setMapInstance(instance) {
      this.mapInstance = instance
    },

    setLoading(loading) {
      this.isLoading = loading
    }
  }
})