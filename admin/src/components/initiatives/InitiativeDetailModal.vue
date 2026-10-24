<!-- admin/src/components/initiatives/InitiativeDetailModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Инициатива #{{ item.id }}</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <div class="modal-body">
        <div class="info-section">
          <div class="info-row">
            <label>Статус:</label>
            <span class="status-badge" :class="`status-${item.status}`">{{ getStatusLabel(item.status) }}</span>
          </div>
          <div class="info-row">
            <label>Категория:</label>
            <span>{{ item.category }}</span>
          </div>
          <div class="info-row">
            <label>Автор:</label>
            <span>{{ item.author }}</span>
          </div>
          <div class="info-row">
            <label>Голосование:</label>
            <div class="votes-display">
              <span class="vote-up"><i class="fas fa-thumbs-up"></i> {{ item.votes_up }}</span>
              <span class="vote-down"><i class="fas fa-thumbs-down"></i> {{ item.votes_down }}</span>
            </div>
          </div>

          <div class="description-block">
            <label>Описание инициативы:</label>
            <p>{{ item.description }}</p>
          </div>

          <div v-if="item.status === 'rejected' && item.reject_reason" class="reject-reason">
            <label>Причина отклонения:</label>
            <p class="text-danger">{{ item.reject_reason }}</p>
          </div>
        </div>

        <div class="actions-section" v-if="item.status === 'pending'">
          <h3>Действия модератора</h3>
          <button class="btn-action btn-approve" @click="handleApprove">
            <i class="fas fa-check"></i> Одобрить (открыть голосование)
          </button>
          <button class="btn-action btn-reject" @click="showRejectForm = true">
            <i class="fas fa-ban"></i> Отклонить
          </button>

          <div v-if="showRejectForm" class="action-form">
            <label>Причина отклонения *</label>
            <textarea v-model="rejectReason" rows="3" placeholder="Укажите причину..."></textarea>
            <div class="form-actions">
              <button class="btn-sm btn-cancel" @click="showRejectForm = false">Отмена</button>
              <button class="btn-sm btn-reject" @click="handleReject" :disabled="!rejectReason.trim()">Отклонить</button>
            </div>
          </div>
        </div>

        <div class="actions-section" v-else-if="item.status === 'approved'">
          <h3>Действия модератора</h3>
          <p class="info-text">Инициатива прошла модерацию и находится на голосовании или рассмотрении.</p>
          <button class="btn-action btn-implement" @click="handleImplement">
            <i class="fas fa-trophy"></i> Отметить как реализованную
          </button>
        </div>

        <div v-else class="actions-section info-only">
          <p><i class="fas fa-info-circle"></i> Обработка этой инициативы завершена.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useInitiativesStore } from '@/stores/initiatives.store'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps({ item: { type: Object, required: true } })
const emit = defineEmits(['close', 'updated'])

const initiativesStore = useInitiativesStore()
const { success, error: showError } = useNotifications()

const showRejectForm = ref(false)
const rejectReason = ref('')

function getStatusLabel(status) {
  const labels = { pending: 'На модерации', approved: 'Одобрена', implemented: 'Реализована', rejected: 'Отклонена' }
  return labels[status] || status
}

async function handleApprove() {
  try {
    await initiativesStore.approveInitiative(props.item.id)
    success('Инициатива одобрена')
    emit('updated')
  } catch { showError('Ошибка') }
}

async function handleReject() {
  try {
    await initiativesStore.rejectInitiative(props.item.id, rejectReason.value)
    success('Инициатива отклонена')
    emit('updated')
  } catch { showError('Ошибка') }
}

async function handleImplement() {
  try {
    await initiativesStore.implementInitiative(props.item.id)
    success('Инициатива отмечена как реализованная! 🎉')
    emit('updated')
  } catch { showError('Ошибка') }
}
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 700px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; display: grid; grid-template-columns: 1.5fr 1fr; gap: 2rem; }
.info-section { display: flex; flex-direction: column; gap: 1rem; }
.info-row { display: flex; gap: 1rem; font-size: 0.9rem; }
.info-row label { color: #70808c; font-weight: 600; min-width: 120px; }

.votes-display { display: flex; gap: 1rem; font-weight: 700; font-size: 1rem; }
.vote-up { color: #06d6a0; }
.vote-down { color: #c64752; }

.description-block, .reject-reason { margin-top: 0.5rem; padding-top: 1rem; border-top: 1px solid #f1f5f9; }
.description-block label, .reject-reason label { display: block; color: #70808c; font-weight: 600; font-size: 0.82rem; margin-bottom: 0.5rem; }
.description-block p { margin: 0; color: #172f40; line-height: 1.6; }
.text-danger { color: #c64752; font-weight: 600; }

.status-badge { display: inline-flex; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; }
.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-approved { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }
.status-implemented { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }

.actions-section { background: #f8fafc; border-radius: 16px; padding: 1.5rem; border: 1px solid #e8edf0; }
.actions-section h3 { margin: 0 0 1.25rem; font-size: 1rem; font-weight: 800; color: #172f40; }
.info-text { color: #70808c; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5; }

.btn-action { width: 100%; padding: 0.85rem; border-radius: 12px; border: none; font-size: 0.9rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: all 0.2s ease; margin-bottom: 0.75rem; }
.btn-approve { background: linear-gradient(135deg, #06d6a0, #05b88a); color: white; }
.btn-approve:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35); }
.btn-reject { background: linear-gradient(135deg, #c64752, #a83a44); color: white; }
.btn-reject:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(198, 71, 82, 0.35); }
.btn-implement { background: linear-gradient(135deg, #00a896, #087e8b); color: white; }
.btn-implement:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }

.action-form { margin-top: 1rem; padding: 1rem; background: white; border-radius: 12px; border: 1px solid #e8edf0; }
.action-form label { display: block; font-size: 0.82rem; font-weight: 700; color: #172f40; margin-bottom: 0.5rem; }
.action-form textarea { width: 100%; border: 1px solid #e8edf0; border-radius: 8px; padding: 0.75rem; font-family: inherit; font-size: 0.9rem; resize: vertical; outline: none; }
.action-form textarea:focus { border-color: #00a896; box-shadow: 0 0 0 3px rgba(0, 168, 150, 0.1); }
.form-actions { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
.btn-sm { flex: 1; padding: 0.6rem; border-radius: 8px; border: none; font-size: 0.82rem; font-weight: 700; cursor: pointer; }
.btn-sm.btn-cancel { background: #f1f5f9; color: #172f40; }
.btn-sm.btn-reject { background: #c64752; color: white; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }

.info-only { color: #70808c; font-size: 0.9rem; line-height: 1.5; background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e8edf0; }
.info-only i { color: #0dcaf0; margin-right: 0.5rem; }

@media (max-width: 767.98px) {
  .modal-body { grid-template-columns: 1fr; }
}
</style>