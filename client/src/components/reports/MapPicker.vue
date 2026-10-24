<!-- client/src/components/reports/MapPicker.vue -->
<template>
  <div class="map-picker-container border rounded-3 overflow-hidden">
    <div ref="mapContainer" class="map-container"></div>
    <div class="p-2 bg-light border-top small text-muted">
      <IconFa name="location-dot" class="me-1" />
      Координаты: {{ coords.lat.toFixed(4) }}, {{ coords.lon.toFixed(4) }}
    </div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'MapPicker',
  components: { IconFa },
  props: {
    modelValue: { type: Object, default: () => ({ lat: 55.43, lon: 37.54 }) }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      map: null,
      marker: null,
      coords: { ...this.modelValue }
    }
  },
  mounted() {
    this.initMap()
  },
  beforeUnmount() {
    if (this.map) this.map.remove()
  },
  methods: {
    initMap() {
      this.map = L.map(this.$refs.mapContainer).setView([this.coords.lat, this.coords.lon], 13)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OSM'
      }).addTo(this.map)

      this.marker = L.marker([this.coords.lat, this.coords.lon], { draggable: true }).addTo(this.map)

      this.marker.on('dragend', (e) => {
        this.updateCoords(e.target.getLatLng())
      })

      this.map.on('click', (e) => {
        this.marker.setLatLng(e.latlng)
        this.updateCoords(e.latlng)
      })
    },
    updateCoords(latlng) {
      this.coords = { lat: latlng.lat, lon: latlng.lng }
      this.$emit('update:modelValue', this.coords)
    }
  }
}
</script>

<style scoped>
.map-container {
  height: 250px;
  width: 100%;
}
</style>