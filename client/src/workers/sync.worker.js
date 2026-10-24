<!-- client/src/views/indoor/IndoorLocationView.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="d-flex align-items-center gap-3 mb-3">
        <button class="btn btn-link text-secondary p-0" @click="$router.back()">
          <IconFa name="arrow-left" size="1.5rem" />
        </button>
        <h4 class="mb-0 fw-bold">Внутренняя карта</h4>
      </div>
    </template>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-civic"></div>
    </div>

    <div v-else>
      <IndoorMapViewer
        :building-id="buildingId"
        :floors="floors"
        :map-layers="mapLayers"
        :zones="zones"
      />
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import IndoorMapViewer from '@/components/map/IndoorMapViewer.vue'
import * as mapsApi from '@/api/maps.api'

export default {
  name: 'IndoorLocationView',
  components: { AppPageContainer, IconFa, IndoorMapViewer },
  props: {
    buildingId: { type: [String, Number], required: true }
  },
  data() {
    return {
      floors: [],
      mapLayers: [],
      zones: [],
      isLoading: false
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.isLoading = true
      try {
        // TODO: Реализовать API для получения данных здания
        // Пока используем мок-данные
        this.floors = [
          { id: 1, level: 1, name: 'Первый этаж' },
          { id: 2, level: 2, name: 'Второй этаж' }
        ]

        this.mapLayers = [
          { id: 1, floor_id: 1, file_url: '/storage/indoor-maps/floor1.png', bounds: [[0, 0], [1000, 1000]] }
        ]

        this.zones = []
      } catch (error) {
        console.error('Failed to load indoor data:', error)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>