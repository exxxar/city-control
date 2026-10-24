<!-- client/src/components/events/EventCard.vue -->
<template>
  <UiCard class="event-card mb-3" hoverable clickable @click="$emit('click', event)">
    <div class="d-flex gap-3">
      <div class="event-date bg-civic text-white rounded p-2 text-center flex-shrink-0" style="width: 70px;">
        <div class="fw-bold" style="font-size: 1.5rem;">{{ day }}</div>
        <div class="small">{{ month }}</div>
      </div>

      <div class="flex-grow-1 min-w-0">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <UiBadge :variant="statusVariant" size="sm">{{ statusText }}</UiBadge>
          <small class="text-muted">{{ formatTime(event.start_date) }}</small>
        </div>

        <h6 class="fw-bold mb-1 text-truncate">{{ event.title }}</h6>
        <p class="text-muted small mb-2 text-truncate">{{ event.description }}</p>

        <div class="d-flex gap-3 text-muted small">
          <span>
            <IconFa name="geo-alt" class="me-1" /> {{ event.location_text || 'Место не указано' }}
          </span>
          <span v-if="event.expected_participants">
            <IconFa name="people" class="me-1" /> {{ event.expected_participants }} участников
          </span>
        </div>
      </div>
    </div>
  </UiCard>
</template>

<script>
import UiCard from '@/components/ui/UiCard.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'EventCard',
  components: { UiCard, UiBadge, IconFa },
  props: {
    event: { type: Object, required: true }
  },
  emits: ['click'],
  computed: {
    day() {
      if (!this.event.start_date) return ''
      return new Date(this.event.start_date).getDate()
    },
    month() {
      if (!this.event.start_date) return ''
      const months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
      return months[new Date(this.event.start_date).getMonth()]
    },
    statusVariant() {
      const map = {
        'draft': 'secondary',
        'pending_approval': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'scheduled': 'info',
        'completed': 'success',
        'cancelled': 'dark'
      }
      return map[this.event.status] || 'secondary'
    },
    statusText() {
      const map = {
        'draft': 'Черновик',
        'pending_approval': 'На согласовании',
        'approved': 'Согласовано',
        'rejected': 'Отклонено',
        'scheduled': 'Запланировано',
        'completed': 'Завершено',
        'cancelled': 'Отменено'
      }
      return map[this.event.status] || this.event.status
    }
  },
  methods: {
    formatTime(date) {
      if (!date) return ''
      return new Date(date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.event-date {
  height: 70px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.bg-civic {
  background: linear-gradient(135deg, #00A896, #007EA7) !important;
}
</style>