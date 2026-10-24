<!-- client/src/components/initiatives/InitiativeCard.vue -->
<template>
  <UiCard class="initiative-card mb-3" hoverable clickable @click="$emit('click', initiative)">
    <div class="d-flex gap-3">
      <div class="initiative-thumb bg-light rounded d-flex align-items-center justify-content-center flex-shrink-0">
        <img v-if="mainImage" :src="mainImage" class="rounded" alt="Фото">
        <IconFa v-else name="lightbulb" size="2rem" color="#FFD166" />
      </div>

      <div class="flex-grow-1 min-w-0">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <UiBadge :variant="statusVariant" size="sm">{{ statusText }}</UiBadge>
          <small class="text-muted">{{ formatDate(initiative.created_at) }}</small>
        </div>

        <h6 class="fw-bold mb-1 text-truncate">{{ initiative.title }}</h6>
        <p class="text-muted small mb-2 text-truncate">{{ initiative.description }}</p>

        <div class="d-flex gap-3 text-muted small">
          <span class="text-warning">
            <IconFa name="hand-thumbs-up-fill" class="me-1" /> {{ initiative.support_count || 0 }} поддержали
          </span>
          <span v-if="initiative.territory">
            <IconFa name="geo-alt" class="me-1" /> {{ initiative.territory.name }}
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
  name: 'InitiativeCard',
  components: { UiCard, UiBadge, IconFa },
  props: {
    initiative: { type: Object, required: true }
  },
  emits: ['click'],
  computed: {
    mainImage() {
      return this.initiative.attachments?.[0]?.file_url || null
    },
    statusVariant() {
      const map = {
        'new': 'secondary',
        'under_review': 'info',
        'accepted': 'success',
        'rejected': 'danger',
        'in_progress': 'warning',
        'completed': 'success'
      }
      return map[this.initiative.status] || 'secondary'
    },
    statusText() {
      const map = {
        'new': 'Новая',
        'under_review': 'На рассмотрении',
        'accepted': 'Принята',
        'rejected': 'Отклонена',
        'in_progress': 'В реализации',
        'completed': 'Реализована'
      }
      return map[this.initiative.status] || this.initiative.status
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU', { day: '2-digit', month: 'short' })
    }
  }
}
</script>

<style scoped>
.initiative-thumb {
  width: 80px;
  height: 80px;
}

.initiative-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>