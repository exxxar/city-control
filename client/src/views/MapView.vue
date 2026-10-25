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

    <!-- Кнопка "Моё местоположение" (мобильная) -->
    <button
      v-if="!selectedProblem"
      class="locate-btn d-md-none"
      @click="locateUser"
      aria-label="Моё местоположение"
    >
      <IconFa name="geo-alt-fill" size="1.25rem" color="var(--civic-primary)" />
    </button>

    <!-- === НОВАЯ КНОПКА МОНИТОРИНГА (справа внизу, над кнопкой геолокации) === -->
    <div class="map-controls-bottom-right">
      <ProximityMonitor
          :is-watching="proximityAlert.isWatching"
          @toggle="handleProximityToggle"
      />
    </div>

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
import ProximityMonitor from '@/components/map/ProximityMonitor.vue' // <-- ИМПОРТ
import ProblemBottomSheet from '@/components/map/ProblemBottomSheet.vue'
import IconFa from '@/components/ui/IconFa.vue'
import { useMapStore } from '@/stores/map.store'
import { useProblemsStore } from
import { useProximityAlert } from '@/composables/useProximityAlert'
import {computed, onUnmounted} from "vue"; // <-- ИМПОРТ

export default {
  name: 'MapView',
  components: { CityMap, ProblemBottomSheet, IconFa,ProximityMonitor },
  setup() {
    const problemsStore = useProblemsStore()

    // Инициализируем composable, передавая ему список проблем и радиус 150 метров
    const proximityAlert = useProximityAlert(
        computed(() => problemsStore.problems),
        150
    )

    // Очищаем память при уходе со страницы
    onUnmounted(() => {
      proximityAlert.stopWatching()
    })

    return {
      proximityAlert
    }
  },
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
    },
    locateUser() {
      if (this.mapInstance?.locate) {
        this.mapInstance.locate({ setView: true, maxZoom: 16 })
      }
    }
  }
}
</script>

<style scoped>
.map-view {
  position: relative;
  height: 100dvh;
  width: 100%;
}

/* Кнопка геолокации (только на мобильных) */
.locate-btn {
  position: absolute;
  bottom: 100px;
  right: 16px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  cursor: pointer;
  transition: transform 0.2s;
}

.locate-btn:active {
  transform: scale(0.95);
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

/* На десктопе скрываем кнопку геолокации (есть в MapControls) */
@media (min-width: 768px) {
  .locate-btn {
    display: none;
  }
}
</style>