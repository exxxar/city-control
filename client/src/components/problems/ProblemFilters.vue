<!-- client/src/components/problems/ProblemFilters.vue -->
<template>
  <div class="problem-filters card shadow-sm mb-3">
    <div class="card-body p-3">
      <div class="row g-2">
        <div class="col-12 col-md-4">
          <UiSelect v-model="localFilters.status" label="Статус" placeholder="Все статусы">
            <option value="">Все статусы</option>
            <option v-for="status in statuses" :key="status.value" :value="status.value">
              {{ status.label }}
            </option>
          </UiSelect>
        </div>

        <div class="col-12 col-md-4">
          <UiSelect v-model="localFilters.category_id" label="Категория" placeholder="Все категории">
            <option value="">Все категории</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </UiSelect>
        </div>

        <div class="col-12 col-md-4">
          <UiSelect v-model="localFilters.priority_id" label="Приоритет" placeholder="Все приоритеты">
            <option value="">Все приоритеты</option>
            <option v-for="priority in priorities" :key="priority.id" :value="priority.id">
              {{ priority.name }}
            </option>
          </UiSelect>
        </div>
      </div>

      <div class="d-flex gap-2 mt-3">
        <UiButton variant="primary" @click="applyFilters">
          <IconFa name="funnel" class="me-2" /> Применить
        </UiButton>
        <UiButton variant="outline-secondary" @click="resetFilters">
          <IconFa name="x-circle" class="me-2" /> Сбросить
        </UiButton>
      </div>
    </div>
  </div>
</template>

<script>
import UiSelect from '@/components/ui/UiSelect.vue'
import UiButton from '@/components/ui/UiButton.vue'
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'ProblemFilters',
  components: { UiSelect, UiButton, IconFa },
  props: {
    categories: { type: Array, default: () => [] },
    priorities: { type: Array, default: () => [] },
    initialFilters: { type: Object, default: () => ({}) }
  },
  emits: ['apply', 'reset'],
  data() {
    return {
      localFilters: {
        status: this.initialFilters.status || '',
        category_id: this.initialFilters.category_id || '',
        priority_id: this.initialFilters.priority_id || ''
      },
      statuses: [
        { value: 'new', label: 'Новая' },
        { value: 'confirmed', label: 'Подтверждена' },
        { value: 'in_progress', label: 'В работе' },
        { value: 'resolved', label: 'Устранена' },
        { value: 'closed', label: 'Закрыта' },
        { value: 'rejected', label: 'Отклонена' }
      ]
    }
  },
  watch: {
    initialFilters: {
      handler(newVal) {
        this.localFilters = { ...newVal }
      },
      deep: true
    }
  },
  methods: {
    applyFilters() {
      this.$emit('apply', { ...this.localFilters })
    },
    resetFilters() {
      this.localFilters = {
        status: '',
        category_id: '',
        priority_id: ''
      }
      this.$emit('reset')
    }
  }
}
</script>