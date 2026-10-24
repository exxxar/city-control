<!-- admin/src/components/events/EventDetailModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>{{ event.title }}</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <div class="modal-body">
        <!-- Левая колонка: Информация -->
        <div class="info-section">
          <div class="info-row">
            <label>Статус:</label>
            <span class="status-badge" :class="`status-${event.status}`">{{ event.statusText }}</span>
          </div>
          <div class="info-row">
            <label>Место проведения:</label>
            <span><i class="fas fa-location-dot"></i> {{ event.location }}</span>
          </div>
          <div class="info-row">
            <label>Дата проведения:</label>
            <span>{{ formatDate(event.event_date) }}</span>
          </div>
          <div class="info-row">
            <label>Организатор:</label>
            <span>{{ event.organizer }}</span>
          </div>
          <div class="info-row">
            <label>Телефон:</label>
            <span>{{ event.organizer_phone }}</span>
          </div>
          <div class="info-row">
            <label>Целевая аудитория:</label>
            <span>{{ event.target_audience || 'Не указана' }}</span>
          </div>
          <div class="info-row">
            <label>Ожидаемое кол-во участников:</label>
            <span class="participants-value">{{ event.participants_count }} чел.</span>
          </div>

          <div class="description-block">
            <label>Описание мероприятия:</label>
            <p>{{ event.description || 'Не указано' }}</p>
          </div>

          <div v-if="event.status === 'rejected' && event.reject_reason" class="reject-reason">
            <label><i class="fas fa-circle-xmark"></i> Причина отклонения:</label>
            <p>{{ event.reject_reason }}</p>
          </div>
        </div>

        <!-- Правая колонка: Действия -->
        <div class="actions-section" v-if="event.status === 'pending'">
          <h3>Действия модератора</h3>

          <button class="btn-action btn-approve" @click="handleApprove">
            <i class="fas fa-check"></i> Согласовать мероприятие
          </button>

          <button class="btn-action btn-reject" @click="showRejectForm = true">
            <i class="fas fa-ban"></i> Отклонить
          </button>

          <div v-if="showRejectForm" class="action-form">
            <label>Причина отклонения *</label>
            <textarea v-model="rejectReason" rows="3" placeholder="Укажите причину отклонения..."></textarea>
            <div class="form-actions">
              <button class="btn-sm btn-cancel" @click="showRejectForm = false">Отмена</button>
              <button class="btn-sm btn-reject" @click="handleReject" :disabled="!rejectReason.trim()">Отклонить</button>
            </div>
          </div>
        </div>

        <div class="actions-section" v-else-if="event.status === 'approved'">
          <h3>Действия модератора</h3>
          <p class="info-text">Мероприятие согласовано и готовится к проведению.</p>
          <button class="btn-action btn-complete" @click="handleComplete">
            <i class="fas fa-flag-checkered"></i> Отметить как завершённое
          </button>
        </div>

        <div class="actions-section" v-else>
          <p class="info-text"><i class="fas fa-info-circle"></i> Обработка этого мероприятия завершена.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import http from '@/api/http'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps({
  event: { type: Object, required: true }
})

const emit = defineEmits(['close', 'updated'])

const { success, error: showError } = useNotifications()

const showRejectForm = ref(false)
const rejectReason = ref('')

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

async function handleApprove() {
  try {
    await http.post(`/admin/events/${props.event.id}/approve`)
    success('Мероприятие согласовано')
    emit('updated')
  } catch (error) {
    showError('Ошибка при согласовании')
  }
}

async function handleReject() {
  try {
    await http.post(`/admin/events/${props.event.id}/reject`, {
      reason: rejectReason.value
    })
    success('Мероприятие отклонено')
    emit('updated')
  } catch (error) {
    showError('Ошибка при отклонении')
  }
}

async function handleComplete() {
  try {
    await http.post(`/admin/events/${props.event.id}/complete`)
    success('Мероприятие отмечено как завершённое')
    emit('updated')
  } catch (error) {
    showError('Ошибка при завершении')
  }
}
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(23, 47, 64, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-card {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid #e8edf0;

  h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
    color: #172f40;
  }
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #f1f5f9;
  color: #70808c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    background: #e2e8f0;
    color: #172f40;
  }
}

.modal-body {
  padding: 1.75rem;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;

  label {
    color: #70808c;
    font-weight: 600;
    min-width: 160px;
  }
}

.participants-value {
  font-weight: 700;
  color: #00a896;
}

.status-badge {
  display: inline-flex;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;

  &.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
  &.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
  &.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }
  &.status-completed { background: rgba(113, 128, 150, 0.12); color: #70808c; }
}

.description-block, .reject-reason {
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;

  label {
    display: block;
    color: #70808c;
    font-weight: 600;
    font-size: 0.82rem;
    margin-bottom: 0.5rem;
  }

  p {
    margin: 0;
    color: #172f40;
    line-height: 1.6;
    font-size: 0.95rem;
  }
}

.reject-reason p {
  color: #c64752;
  font-weight: 600;
}

.reject-reason i {
  margin-right: 0.5rem;
}

.actions-section {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e8edf0;

  h3 {
    margin: 0 0 1.25rem;
    font-size: 1rem;
    font-weight: 800;
    color: #172f40;
  }
}

.info-text {
  color: #70808c;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.5;

  i {
    color: #0dcaf0;
    margin-right: 0.5rem;
  }
}

.btn-action {
  width: 100%;
  padding: 0.85rem;
  border-radius: 12px;
  border: none;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  margin-bottom: 0.75rem;

  &.btn-approve {
    background: linear-gradient(135deg, #06d6a0, #05b88a);
    color: white;
    box-shadow: 0 4px 12px rgba(6, 214, 160, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35);
    }
  }

  &.btn-reject {
    background: linear-gradient(135deg, #c64752, #a83a44);
    color: white;
    box-shadow: 0 4px 12px rgba(198, 71, 82, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(198, 71, 82, 0.35);
    }
  }

  &.btn-complete {
    background: linear-gradient(135deg, #00a896, #087e8b);
    color: white;
    box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
    }
  }
}

.action-form {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e8edf0;

  label {
    display: block;
    font-size: 0.82rem;
    font-weight: 700;
    color: #172f40;
    margin-bottom: 0.5rem;
  }

  textarea {
    width: 100%;
    border: 1px solid #e8edf0;
    border-radius: 8px;
    padding: 0.75rem;
    font-family: inherit;
    font-size: 0.9rem;
    resize: vertical;
    outline: none;

    &:focus {
      border-color: #00a896;
      box-shadow: 0 0 0 3px rgba(0, 168, 150, 0.1);
    }
  }
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.btn-sm {
  flex: 1;
  padding: 0.6rem;
  border-radius: 8px;
  border: none;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;

  &.btn-cancel {
    background: #f1f5f9;
    color: #172f40;
  }

  &.btn-reject {
    background: #c64752;
    color: white;

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

@media (max-width: 767.98px) {
  .modal-body {
    grid-template-columns: 1fr;
  }
}
</style>