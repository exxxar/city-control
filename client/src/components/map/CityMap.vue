<!-- client/src/components/map/CityMap.vue -->
<template>
  <div class="city-map-container position-relative">
    <div ref="mapContainer" class="map-wrapper"></div>

    <!-- Controls overlay (Top Right) -->
    <div class="map-controls-overlay">
      <slot name="controls">
        <MapControls
            @locate="handleLocate"
            @toggle-layer="handleToggleLayer"
            @zoom-in="map?.zoomIn()"
            @zoom-out="map?.zoomOut()"
        />
      </slot>
    </div>

    <!-- Legend overlay (Bottom Left) -->
    <div class="map-legend-overlay">
      <slot name="legend">
        <MapLegend />
      </slot>
    </div>

    <!-- Home button overlay (Bottom Right) -->
    <div class="home-button-overlay">
      <button class="control-btn home-btn" @click="goToHome" title="На главную">
        <IconFa name="house" size="1.25rem" />
      </button>
    </div>

    <!-- Bottom sheet slot -->
    <slot name="bottom-sheet"></slot>
  </div>
</template>

<script>
import * as L from 'leaflet'
import 'leaflet.markercluster/dist/leaflet.markercluster.js'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import MapControls from './MapControls.vue'
import MapLegend from './MapLegend.vue'
import IconFa from '@/components/ui/IconFa.vue' // <-- Добавлен импорт иконки
import { useMapStore } from '@/stores/map.store'

export default {
  name: 'CityMap',
  components: {
    MapControls,
    MapLegend,
    IconFa // <-- Добавлен в компоненты
  },
  props: {
    center: {
      type: Array,
      default: () => [55.4315, 37.5460] // Подольск
    },
    zoom: {
      type: Number,
      default: 14
    },
    enableClustering: {
      type: Boolean,
      default: true
    }
  },
  emits: ['map-ready', 'marker-click', 'location-found'],
  data() {
    return {
      map: null,
      markerClusterGroup: null,
      userLocationMarker: null,
      layers: {
        osm: null,
        satellite: null
      }
    }
  },
  computed: {
    mapStore() {
      return useMapStore()
    }
  },
  mounted() {
    this.initMap()
  },
  beforeUnmount() {
    this.destroyMap()
  },
  methods: {
    initMap() {
      // Инициализация карты
      this.map = L.map(this.$refs.mapContainer, {
        center: this.center,
        zoom: this.zoom,
        zoomControl: false // Скрываем стандартные контролы
      })

      // Слои карты
      this.layers.osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      })

      this.layers.satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '© Esri',
        maxZoom: 18
      })

      this.layers.osm.addTo(this.map)

      // Кластеризация маркеров
      if (this.enableClustering) {
        this.markerClusterGroup = L.markerClusterGroup({
          maxClusterRadius: 50,
          spiderfyOnMaxZoom: true,
          showCoverageOnHover: false,
          zoomToBoundsOnClick: true
        })
        this.map.addLayer(this.markerClusterGroup)
      }

      // Сохраняем инстанс в store
      this.mapStore.setMapInstance(this.map)

      // Слушаем события карты
      this.map.on('moveend', () => {
        const center = this.map.getCenter()
        this.mapStore.setCenter([center.lat, center.lng])
        this.mapStore.setZoom(this.map.getZoom())
      })

      this.$emit('map-ready', this.map)
    },

    addMarker(lat, lng, options = {}) {
      const marker = L.marker([lat, lng], options)

      if (options.popup) {
        marker.bindPopup(options.popup)
      }

      marker.on('click', () => {
        this.$emit('marker-click', options.data || marker)
      })

      if (this.enableClustering && this.markerClusterGroup) {
        this.markerClusterGroup.addLayer(marker)
      } else {
        marker.addTo(this.map)
      }

      return marker
    },

    clearMarkers() {
      if (this.markerClusterGroup) {
        this.markerClusterGroup.clearLayers()
      }
    },

    handleLocate() {
      this.map.locate({ setView: true, maxZoom: 16 })

      this.map.on('locationfound', (e) => {
        if (this.userLocationMarker) {
          this.map.removeLayer(this.userLocationMarker)
        }

        this.userLocationMarker = L.circleMarker([e.latlng.lat, e.latlng.lng], {
          radius: 10,
          fillColor: '#00A896',
          color: '#fff',
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(this.map)

        this.mapStore.setUserLocation([e.latlng.lat, e.latlng.lng])
        this.$emit('location-found', { lat: e.latlng.lat, lng: e.latlng.lng })
      })

      this.map.on('locationerror', (e) => {
        console.error('Location error:', e.message)
        alert('Не удалось определить местоположение')
      })
    },

    handleToggleLayer(layerName) {
      Object.values(this.layers).forEach(layer => {
        if (this.map.hasLayer(layer)) {
          this.map.removeLayer(layer)
        }
      })

      if (this.layers[layerName]) {
        this.layers[layerName].addTo(this.map)
      }
    },

    flyTo(lat, lng, zoom = 16) {
      this.map.flyTo([lat, lng], zoom)
    },

    // <-- НОВЫЙ МЕТОД для перехода на главную
    goToHome() {
      this.$router.push('/')
    },

    destroyMap() {
      if (this.map) {
        this.map.remove()
        this.map = null
      }
    }
  }
}
</script>

<style scoped>
.city-map-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-wrapper {
  width: 100%;
  height: 100%;
  z-index: 1;
}

.map-controls-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.map-legend-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 1000;
}

/* === Стили для кнопки "Домой" === */
.home-button-overlay {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.home-btn {
  background: white;
  border: 1px solid #e9ecef;
  padding:10px;
  border-radius: 5px;
}

.home-btn:hover {
  background: var(--civic-primary, #00A896);
  color: white;
  border-color: var(--civic-primary, #00A896);
}

/* Адаптация для мобильных устройств */
@media (max-width: 768px) {
  .map-controls-overlay {
    top: 10px;
    right: 10px;
  }

  .map-legend-overlay {
    bottom: 10px;
    left: 10px;
  }

  .home-button-overlay {
    bottom: 10px;
    right: 10px;
  }
}
</style>