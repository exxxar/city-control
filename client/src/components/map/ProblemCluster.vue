<!-- client/src/components/map/ProblemCluster.vue -->
<template>
  <div></div>
</template>

<script>
import * as L from 'leaflet'
import 'leaflet.markercluster/dist/leaflet.markercluster.js'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

export default {
  name: 'ProblemCluster',
  props: {
    map: { type: Object, required: true },
    problems: { type: Array, default: () => [] }
  },
  emits: ['marker-click'],
  data() {
    return {
      clusterGroup: null
    }
  },
  watch: {
    problems: {
      handler(newProblems) {
        this.renderMarkers(newProblems)
      },
      deep: true
    }
  },
  mounted() {
    this.clusterGroup = L.markerClusterGroup({
      maxClusterRadius: 50,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false
    })
    this.map.addLayer(this.clusterGroup)
    this.renderMarkers(this.problems)
  },
  beforeUnmount() {
    if (this.clusterGroup) {
      this.map.removeLayer(this.clusterGroup)
    }
  },
  methods: {
    renderMarkers(problems) {
      this.clusterGroup.clearLayers()

      problems.forEach(problem => {
        if (problem.geo_tag?.latitude && problem.geo_tag?.longitude) {
          const marker = L.marker([problem.geo_tag.latitude, problem.geo_tag.longitude])
          marker.on('click', () => {
            this.$emit('marker-click', problem)
          })
          this.clusterGroup.addLayer(marker)
        }
      })
    }
  }
}
</script>