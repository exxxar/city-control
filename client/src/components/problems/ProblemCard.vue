<!-- client/src/components/problems/ProblemCard.vue -->
<template>
  <UiCard class="problem-card mb-3" hoverable clickable @click="$emit('click', problem)">
    <div class="d-flex gap-3">
      <!-- Thumbnail -->
      <div class="problem-thumb bg-light rounded d-flex align-items-center justify-content-center flex-shrink-0">
        <img v-if="mainImage" :src="mainImage" class="rounded" alt="Фото">
        <IconFa v-else name="image" size="2rem" color="#adb5bd" />
      </div>

      <!-- Content -->
      <div class="flex-grow-1 min-w-0">
        <div class="d-flex justify-content-between align-items-start mb-1">
          <ProblemStatusBadge :status="problem.status" size="sm" />
          <small class="text-muted">{{ formatDate(problem.created_at) }}</small>
        </div>

        <h6 class="fw-bold mb-1 text-truncate">{{ problem.title }}</h6>
        <p class="text-muted small mb-2 text-truncate">{{ problem.description }}</p>

        <div class="d-flex gap-3 text-muted small">
          <span>
            <IconFa name="chat-dots" class="me-1" /> {{ problem.messages_count || 0 }}
          </span>
          <span>
            <IconFa name="people" class="me-1" /> {{ problem.confirmations_count || 0 }}
          </span>
          <span v-if="problem.rating">
            <IconFa name="star-fill" color="#FFD166" class="me-1" /> {{ problem.rating.toFixed(1) }}
          </span>
        </div>
      </div>
    </div>
  </UiCard>
</template>

<script>
import UiCard from '@/components/ui/UiCard.vue'
import IconFa from '@/components/ui/IconFa.vue'
import ProblemStatusBadge from './ProblemStatusBadge.vue'

export default {
  name: 'ProblemCard',
  components: { UiCard, IconFa, ProblemStatusBadge },
  props: {
    problem: { type: Object, required: true }
  },
  emits: ['click'],
  computed: {
    mainImage() {
      return this.problem.attachments?.[0]?.file_url || null
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
.problem-thumb {
  width: 80px;
  height: 80px;
}

.problem-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>