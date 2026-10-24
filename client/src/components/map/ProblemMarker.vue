<!-- client/src/components/map/ProblemMarker.vue -->
<template>
  <div :class="['problem-marker', markerClass]" @click="$emit('click', problem)">
    <IconFa :name="statusIcon" size="1.25rem" color="white" />
    <div v-if="problem.confirmations_count > 0" class="marker-badge">
      {{ problem.confirmations_count }}
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'ProblemMarker',
  components: { IconFa },
  props: {
    problem: {
      type: Object,
      required: true
    }
  },
  emits: ['click'],
  computed: {
    markerClass() {
      const status = this.problem.status
      const priority = this.problem.priority_id

      // Критическая проблема (приоритет 1)
      if (priority === 1) return 'marker-critical'

      // Статусы
      if (['new', 'needs_clarification'].includes(status)) return 'marker-new'
      if (['confirmed', 'transferred', 'accepted'].includes(status)) return 'marker-confirmed'
      if (['in_progress', 'suspended'].includes(status)) return 'marker-in-progress'
      if (['solution_ready', 'awaiting_confirmation'].includes(status)) return 'marker-ready'
      if (['resolved', 'closed'].includes(status)) return 'marker-resolved'
      if (status === 'rejected') return 'marker-rejected'

      return 'marker-default'
    },
    statusIcon() {
      const status = this.problem.status

      if (['new', 'needs_clarification'].includes(status)) return 'exclamation-circle'
      if (['confirmed', 'transferred', 'accepted'].includes(status)) return 'check-circle'
      if (['in_progress', 'suspended'].includes(status)) return 'gear'
      if (['solution_ready', 'awaiting_confirmation'].includes(status)) return 'hourglass-split'
      if (['resolved', 'closed'].includes(status)) return 'check2-all'
      if (status === 'rejected') return 'x-circle'

      return 'question-circle'
    }
  }
}
</script>

<style scoped>
.problem-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  border: 3px solid white;
  transition: transform 0.2s;
  position: relative;
}

.problem-marker:hover {
  transform: scale(1.1);
}

.marker-critical {
  background: linear-gradient(135deg, #EF476F, #D63384);
}

.marker-new {
  background: linear-gradient(135deg, #6c757d, #495057);
}

.marker-confirmed {
  background: linear-gradient(135deg, #0dcaf0, #0aa2c0);
}

.marker-in-progress {
  background: linear-gradient(135deg, #FFD166, #FFC107);
}

.marker-ready {
  background: linear-gradient(135deg, #00A896, #007EA7);
}

.marker-resolved {
  background: linear-gradient(135deg, #06D6A0, #05B384);
}

.marker-rejected {
  background: linear-gradient(135deg, #adb5bd, #6c757d);
}

.marker-default {
  background: linear-gradient(135deg, #00A896, #007EA7);
}

.marker-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #EF476F;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 2px solid white;
}
</style>