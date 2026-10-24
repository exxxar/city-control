<!-- client/src/components/map/MapControls.vue -->
<template>
  <div class="map-controls d-flex flex-column gap-2">
    <!-- Locate me -->
    <button
        class="control-btn"
        @click="$emit('locate')"
        title="Моё местоположение"
    >
      <IconFa name="location-dot" size="1.25rem" />
    </button>

    <!-- Zoom controls -->
    <div class="control-group">
      <button class="control-btn" @click="$emit('zoom-in')" title="Приблизить">
        <IconFa name="plus" size="1.25rem" />
      </button>
      <button class="control-btn" @click="$emit('zoom-out')" title="Отдалить">
        <IconFa name="minus" size="1.25rem" />
      </button>
    </div>

    <!-- Layer switcher -->
    <div class="control-group">
      <button
          class="control-btn"
          :class="{ active: currentLayer === 'osm' }"
          @click="switchLayer('osm')"
          title="Схема"
      >
        <IconFa name="map" size="1.25rem" />
      </button>
      <button
          class="control-btn"
          :class="{ active: currentLayer === 'satellite' }"
          @click="switchLayer('satellite')"
          title="Спутник"
      >
        <IconFa name="globe" size="1.25rem" />
      </button>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'MapControls',
  components: { IconFa },
  emits: ['locate', 'zoom-in', 'zoom-out', 'toggle-layer'],
  data() {
    return {
      currentLayer: 'osm'
    }
  },
  methods: {
    switchLayer(layer) {
      this.currentLayer = layer
      this.$emit('toggle-layer', layer)
    }
  }
}
</script>

<style scoped>
.map-controls {
  background: white;
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.control-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #495057;
}

.control-btn:hover {
  background: #f8f9fa;
  color: var(--civic-primary, #00A896);
}

.control-btn.active {
  background: var(--civic-primary, #00A896);
  color: white;
}

.control-group {
  display: flex;
  flex-direction: column;
  border-top: 1px solid #e9ecef;
  padding-top: 8px;
  margin-top: 8px;
}

.control-group:first-child {
  border-top: none;
  padding-top: 0;
  margin-top: 0;
}
</style>