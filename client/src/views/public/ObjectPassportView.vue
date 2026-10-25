<!-- client/src/views/public/ObjectPassportView.vue -->
<template>

    <div class="container py-4">
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-civic"></div>
      </div>

      <div v-else-if="object" class="object-passport">
        <!-- Header -->
        <div class="card mb-4">
          <div class="card-body">
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="bg-civic text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                <IconFa name="building" size="2rem" />
              </div>
              <div>
                <h4 class="mb-1 fw-bold">{{ object.name }}</h4>
                <p class="text-muted mb-0">{{ object.address }}</p>
              </div>
            </div>

            <div class="d-flex gap-2">
              <UiBadge variant="primary">
                <IconFa name="qr-code" class="me-1" /> QR: {{ object.qr_token?.substring(0, 8) }}
              </UiBadge>
              <UiBadge variant="secondary">
                <IconFa name="geo-alt" class="me-1" /> {{ object.coordinates }}
              </UiBadge>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <ul class="nav nav-tabs mb-3">
          <li class="nav-item">
            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#problems">
              Проблемы ({{ problems.length }})
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#initiatives">
              Инициативы ({{ initiatives.length }})
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#events">
              Мероприятия ({{ events.length }})
            </button>
          </li>
        </ul>

        <!-- Tab content -->
        <div class="tab-content">
          <div class="tab-pane fade show active" id="problems">
            <div v-if="problems.length === 0" class="text-center py-4">
              <IconFa name="check-circle" size="2rem" color="#06D6A0" />
              <p class="text-muted mt-2">Нет активных проблем</p>
            </div>
            <div v-else>
              <ProblemCard
                v-for="problem in problems"
                :key="problem.id"
                :problem="problem"
                @click="openProblem"
              />
            </div>
          </div>

          <div class="tab-pane fade" id="initiatives">
            <div v-if="initiatives.length === 0" class="text-center py-4">
              <p class="text-muted">Нет инициатив для этого объекта</p>
            </div>
          </div>

          <div class="tab-pane fade" id="events">
            <div v-if="events.length === 0" class="text-center py-4">
              <p class="text-muted">Нет мероприятий для этого объекта</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <IconFa name="exclamation-triangle" size="3rem" color="#adb5bd" />
        <p class="text-muted mt-3">Объект не найден</p>
      </div>
    </div>

</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'
import UiBadge from '@/components/ui/UiBadge.vue'
import ProblemCard from '@/components/problems/ProblemCard.vue'
import * as mapsApi from '@/api/maps.api'
import * as problemsApi from '@/api/problems.api'

export default {
  name: 'ObjectPassportView',
  components: { PublicLayout, IconFa, UiBadge, ProblemCard },
  props: {
    id: { type: [String, Number], required: true }
  },
  data() {
    return {
      object: null,
      problems: [],
      initiatives: [],
      events: [],
      isLoading: false
    }
  },
  async mounted() {
    await this.loadObjectPassport()
  },
  methods: {
    async loadObjectPassport() {
      this.isLoading = true
      try {
        // TODO: Реализовать API для паспорта объекта
        // Пока используем мок-данные
        this.object = {
          id: this.id,
          name: 'Администрация города',
          address: 'ул. Ленина, д. 10',
          qr_token: 'abc123def456',
          coordinates: '55.43, 37.54'
        }

        this.problems = await problemsApi.getProblems({ object_id: this.id })
      } catch (error) {
        console.error('Failed to load object passport:', error)
      } finally {
        this.isLoading = false
      }
    },

    openProblem(problem) {
      this.$router.push({ name: 'ProblemPublic', params: { id: problem.id } })
    }
  }
}
</script>