<!-- client/src/components/map/GeoTagLayer.vue -->
<template>
  <div></div>
</template>

<script>
import L from 'leaflet'

export default {
  name: 'GeoTagLayer',
  props: {
    map: {
      type: Object,
      required: true
    },
    geoTags: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      layerGroup: null
    }
  },
  watch: {
    geoTags: {
      handler(newTags) {
        this.renderGeoTags(newTags)
      },
      deep: true
    }
  },
  mounted() {
    this.layerGroup = L.layerGroup().addTo(this.map)
    this.renderGeoTags(this.geoTags)
  },
  beforeUnmount() {
    if (this.layerGroup) {
      this.map.removeLayer(this.layerGroup)
    }
  },
  methods: {
    renderGeoTags(tags) {
      this.layerGroup.clearLayers()

      tags.forEach(tag => {
        if (!tag.active) return

        if (tag.type === 'gps' && tag.latitude && tag.longitude) {
          this.renderGpsTag(tag)
        } else if (tag.type === 'polygon' && tag.geometry) {
          this.renderPolygonTag(tag)
        } else if (tag.type === 'qr') {
          this.renderQrTag(tag)
        }
      })
    },

    renderGpsTag(tag) {
      const circle = L.circle([tag.latitude, tag.longitude], {
        radius: tag.notification_radius || tag.radius || 50,
        color: '#00A896',
        fillColor: '#00A896',
        fillOpacity: 0.2,
        weight: 2
      })

      circle.bindPopup(`
        <div class="p-2">
          <strong>Гео-метка</strong><br>
          Тип: GPS<br>
          Радиус: ${tag.radius || 50}м
        </div>
      `)

      this.layerGroup.addLayer(circle)
    },

    renderPolygonTag(tag) {
      if (!tag.geometry?.coordinates) return

      const coords = tag.geometry.coordinates[0].map(c => [c[1], c[0]])
      const polygon = L.polygon(coords, {
        color: '#FFD166',
        fillColor: '#FFD166',
        fillOpacity: 0.3,
        weight: 2
      })

      polygon.bindPopup(`
        <div class="p-2">
          <strong>Зона</strong><br>
          Тип: Полигон
        </div>
      `)

      this.layerGroup.addLayer(polygon)
    },

    renderQrTag(tag) {
      if (!tag.building_id) return

      const marker = L.marker([55.43, 37.54], {
        icon: L.divIcon({
          className: 'qr-marker',
          html: '<div class="qr-icon"><i class="bi bi-qr-code"></i></div>',
          iconSize: [30, 30]
        })
      })

      marker.bindPopup(`
        <div class="p-2">
          <strong>QR-метка</strong><br>
          Токен: ${tag.qr_token}
        </div>
      `)

      this.layerGroup.addLayer(marker)
    }
  }
}
</script>

<style>
.qr-icon {
  width: 30px;
  height: 30px;
  background: white;
  border: 2px solid #00A896;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: #00A896;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
</style>