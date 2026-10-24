<!-- client/src/components/map/IndoorMapViewer.vue -->
<template>
  <div class="indoor-map-viewer">
    <!-- Floor selector -->
    <div class="floor-selector card shadow-sm mb-3">
      <div class="card-body p-2">
        <div class="d-flex gap-2 overflow-auto">
          <button
            v-for="floor in floors"
            :key="floor.id"
            :class="['floor-btn', { active: selectedFloor?.id === floor.id }]"
            @click="selectFloor(floor)"
          >
            {{ floor.name || `Этаж ${floor.level}` }}
          </button>
        </div>
      </div>
    </div>

    <!-- Map container -->
    <div ref="indoorMapContainer" class="indoor-map-container"></div>
  </div>
</template>

<script>
import L from 'leaflet'

export default {
  name: 'IndoorMapViewer',
  props: {
    buildingId: { type: Number, required: true },
    floors: { type: Array, default: () => [] },
    mapLayers: { type: Array, default: () => [] },
    zones: { type: Array, default: () => [] }
  },
  data() {
    return {
      map: null,
      selectedFloor: null,
      imageOverlay: null,
      zoneLayer: null
    }
  },
  watch: {
    selectedFloor(newFloor) {
      if (newFloor) this.loadFloorMap(newFloor)
    }
  },
  mounted() {
    this.initMap()
    if (this.floors.length > 0) this.selectFloor(this.floors[0])
  },
  beforeUnmount() {
    if (this.map) this.map.remove()
  },
  methods: {
    initMap() {
      this.map = L.map(this.$refs.indoorMapContainer, {
        crs: L.CRS.Simple,
        minZoom: -2,
        maxZoom: 2
      })
      this.zoneLayer = L.layerGroup().addTo(this.map)
    },
    selectFloor(floor) {
      this.selectedFloor = floor
    },
    loadFloorMap(floor) {
      const layer = this.mapLayers.find(l => l.floor_id === floor.id)
      if (!layer) return

      if (this.imageOverlay) this.map.removeLayer(this.imageOverlay)

      // Загрузка изображения плана этажа
      const imageUrl = layer.file_url
      const bounds = layer.bounds || [[0, 0], [1000, 1000]] // Дефолтные границы

      this.imageOverlay = L.imageOverlay(imageUrl, bounds).addTo(this.map)
      this.map.fitBounds(bounds)

      // Загрузка зон этого этажа
      this.loadFloorZones(floor.id)
    },
    loadFloorZones(floorId) {
      this.zoneLayer.clearLayers()

      const floorZones = this.zones.filter(z => {
        // Упрощенная фильтрация: зоны, связанные с этим этажом
        return z.map_layer?.floor_id === floorId
      })

      floorZones.forEach(zone => {
        if (zone.geometry?.coordinates) {
          const coords = zone.geometry.coordinates[0].map(c => [c[1], c[0]])
          const polygon = L.polygon(coords, {
            color: '#00A896',
            fillColor: '#00A896',
            fillOpacity: 0.2,
            weight: 2
          })
          polygon.bindPopup(`<strong>${zone.name}</strong>`)
          this.zoneLayer.addLayer(polygon)
        }
      })
    }
  }
}
</script>

<style scoped>
.indoor-map-container {
  width: 100%;
  height: 500px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e9ecef;
}

.floor-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  background: white;
  border-radius: 8px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s;
}

.floor-btn:hover {
  background: #f8f9fa;
}

.floor-btn.active {
  background: var(--civic-primary, #00A896);
  color: white;
  border-color: var(--civic-primary, #00A896);
}
</style>