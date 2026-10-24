<!-- client/src/components/problems/ProblemTimeline.vue -->
<template>
  <div class="problem-timeline">
    <div v-for="(item, index) in history" :key="index" class="timeline-item d-flex gap-3 mb-3">
      <div class="timeline-icon d-flex flex-column align-items-center">
        <div :class="['icon-circle', `bg-${getVariant(item.new_status)}`]">
          <IconFa :name="getIcon(item.new_status)" size="0.875rem" color="white" />
        </div>
        <div v-if="index < history.length - 1" class="timeline-line"></div>
      </div>

      <div class="timeline-content flex-grow-1 pb-3">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <strong class="small">{{ getActionText(item) }}</strong>
            <p v-if="item.comment" class="text-muted small mb-0 mt-1">{{ item.comment }}</p>
          </div>
          <small class="text-muted text-nowrap ms-2">{{ formatDateTime(item.created_at) }}</small>
        </div>
        <div class="text-muted small mt-1">
          {{ item.changed_by?.full_name || 'Система' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'ProblemTimeline',
  components: { IconFa },
  props: {
    history: { type: Array, default: () => [] }
  },
  methods: {
    getVariant(status) {
      const map = {
        'new': 'secondary', 'in_progress': 'warning', 'resolved': 'success', 'rejected': 'danger'
      }
      return map[status] || 'primary'
    },
    getIcon(status) {
      const map = {
        'new': 'plus-circle', 'in_progress': 'gear', 'resolved': 'check-circle', 'rejected': 'x-circle'
      }
      return map[status] || 'circle'
    },
    getActionText(item) {
      if (!item.old_status) return 'Проблема создана'
      return `Статус изменён: ${item.old_status} → ${item.new_status}`
    },
    formatDateTime(date) {
      if (!date) return ''
      return new Date(date).toLocaleString('ru-RU', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.timeline-line {
  width: 2px;
  flex-grow: 1;
  background: #e9ecef;
  margin-top: 4px;
}
</style>