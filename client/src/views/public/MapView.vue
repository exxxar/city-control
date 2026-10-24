<!-- client/src/views/public/MapView.vue -->
<template>
  <div class="map-view">
    <CityMap
      :center="mapStore.center"
      :zoom="mapStore.zoom"
      :problems="problems"
      @map-ready="onMapReady"
      @marker-click="onMarkerClick"
      @location-found="onLocationFound"
    >
      <template #bottom-sheet>
        <ProblemBottomSheet
          :problem="selectedProblem"
          @close="closeBottomSheet"
          @confirm="onProblemConfirmed"
        />
      </template>
    </CityMap>

    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border text-civic" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>
  </div>
</template>

<script>
import CityMap from '@/components/map/CityMap.vue'
import ProblemBottomSheet from '@/components/map/ProblemBottomSheet.vue'
import { useMapStore } from '@/stores/map.store'
import { useProblemsStore } from '@/stores/problems.store'

export default {
  name: 'MapView',
  components: { CityMap, ProblemBottomSheet },
  data() {
    return {
      mapInstance: null,
      selectedProblem: null,
      isLoading: false
    }
  },
  computed: {
    mapStore() { return useMapStore() },
    problemsStore() { return useProblemsStore() },
    problems() { return this.problemsStore.problems }
  },
  async mounted() {
    await this.loadProblems()
  },
  methods: {
    async loadProblems() {
      this.isLoading = true
      try {
        await this.problemsStore.fetchProblems({ page: 1, per_page: 100 })
      } catch (error) {
        console.error('Failed to load problems:', error)
      } finally {
        this.isLoading = false
      }
    },
    onMapReady(map) { this.mapInstance = map },
    onMarkerClick(problem) { this.selectedProblem = problem },
    closeBottomSheet() { this.selectedProblem = null },
    onProblemConfirmed(problemId) {
      console.log('Problem confirmed:', problemId)
      this.closeBottomSheet()
    },
    onLocationFound(location) {
      console.log('User location:', location)
    }
  }
}
</script>

<style scoped>
.map-view {
  position: relative;
  width: 100%;
  height: 100%; /* ← Занимает весь родительский контейнер */
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.text-civic {
  color: var(--civic-primary, #00A896);
}
</style>