<template>
  <div class="proximity-monitor" :class="{ 'is-active': isWatching }">
    <button
        class="monitor-btn"
        @click="toggleMonitoring"
        :title="isWatching ? 'Отключить оповещения о проблемах рядом' : 'Включить оповещения о проблемах рядом'"
    >
      <IconFa :name="isWatching ? 'bell' : 'bell-slash'" />
      <span v-if="isWatching" class="pulse-ring"></span>
    </button>

    <div v-if="isWatching" class="monitor-tooltip">
      Оповещения включены (радиус 150м)
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'ProximityMonitor',
  components: { IconFa },
  props: {
    isWatching: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggle'],
  methods: {
    toggleMonitoring() {
      this.$emit('toggle', !this.isWatching)
    }
  }
}
</script>

<style scoped>
.proximity-monitor {
  position: relative;
}

.monitor-btn {
  position: relative;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid #e8edf0;
  background: #ffffff;
  color: #70808c;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  font-size: 1.2rem;
}

.monitor-btn:hover {
  background: #f8fffe;
  color: #00a896;
  border-color: #00a896;
}

/* Состояние "Активно" */
.proximity-monitor.is-active .monitor-btn {
  background: #00a896;
  color: #ffffff;
  border-color: #00a896;
}

/* Анимация пульсации для активного режима */
.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #00a896;
  animation: pulse 2s infinite;
  pointer-events: none;
}

@keyframes pulse {
  0% { width: 100%; height: 100%; opacity: 1; }
  100% { width: 160%; height: 160%; opacity: 0; }
}

.monitor-tooltip {
  position: absolute;
  right: 60px;
  top: 50%;
  transform: translateY(-50%);
  background: #172f40;
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8rem;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.proximity-monitor:hover .monitor-tooltip {
  opacity: 1;
}
</style>