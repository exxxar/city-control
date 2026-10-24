<!-- client/src/components/map/MapLegend.vue -->
<template>
  <div class="map-legend card shadow-sm" v-if="isVisible">
    <div class="card-body p-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h6 class="mb-0 fw-bold small">Легенда</h6>
        <button class="btn btn-sm btn-link text-secondary p-0" @click="toggle">
          <IconFa :name="isVisible ? 'chevron-down' : 'chevron-up'" size="0.875rem" />
        </button>
      </div>

      <div v-show="isExpanded" class="legend-items">
        <div class="legend-item">
          <div class="legend-marker marker-critical"></div>
          <span class="small">Критическая</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker marker-new"></div>
          <span class="small">Новая</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker marker-confirmed"></div>
          <span class="small">Подтверждена</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker marker-in-progress"></div>
          <span class="small">В работе</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker marker-ready"></div>
          <span class="small">Решение готово</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker marker-resolved"></div>
          <span class="small">Устранена</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'MapLegend',
  components: { IconFa },
  data() {
    return {
      isVisible: true,
      isExpanded: true
    }
  },
  methods: {
    toggle() {
      this.isExpanded = !this.isExpanded
    }
  }
}
</script>

<style scoped>
.map-legend {
  max-width: 200px;
  border-radius: 12px;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-marker {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.marker-critical { background: #EF476F; }
.marker-new { background: #6c757d; }
.marker-confirmed { background: #0dcaf0; }
.marker-in-progress { background: #FFD166; }
.marker-ready { background: #00A896; }
.marker-resolved { background: #06D6A0; }

@media (max-width: 768px) {
  .map-legend {
    max-width: 160px;
  }

  .legend-item span {
    font-size: 0.7rem;
  }
}
</style>