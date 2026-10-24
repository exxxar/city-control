<!-- client/src/components/problems/ProblemStatusBadge.vue -->
<template>
  <UiBadge :variant="variant" :size="size">
    {{ statusText }}
  </UiBadge>
</template>

<script>
import UiBadge from '@/components/ui/UiBadge.vue'

export default {
  name: 'ProblemStatusBadge',
  components: { UiBadge },
  props: {
    status: { type: String, required: true },
    size: { type: String, default: 'md' }
  },
  computed: {
    variant() {
      const map = {
        'new': 'secondary',
        'needs_clarification': 'warning',
        'confirmed': 'info',
        'transferred': 'info',
        'accepted': 'info',
        'in_progress': 'warning',
        'suspended': 'dark',
        'solution_ready': 'primary',
        'awaiting_confirmation': 'primary',
        'resolved': 'success',
        'closed': 'success',
        'rejected': 'danger'
      }
      return map[this.status] || 'secondary'
    },
    statusText() {
      const map = {
        'new': 'Новая',
        'needs_clarification': 'Уточнение',
        'confirmed': 'Подтверждена',
        'transferred': 'Передана',
        'accepted': 'Принята',
        'in_progress': 'В работе',
        'suspended': 'Пауза',
        'solution_ready': 'Решение готово',
        'awaiting_confirmation': 'Ожидает проверки',
        'resolved': 'Устранена',
        'closed': 'Закрыта',
        'rejected': 'Отклонена'
      }
      return map[this.status] || this.status
    }
  }
}
</script>