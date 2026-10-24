<!-- admin/src/components/problems/ProblemDetailModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Обращение #{{ problem.id }}</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <div class="modal-body">
        <!-- Левая колонка: Информация -->
        <div class="info-section">
          <div class="info-row">
            <label>Статус:</label>
            <span class="status-badge" :class="`status-${problem.status}`">{{ getStatusLabel(problem.status) }}</span>
          </div>
          <div class="info-row">
            <label>Категория:</label>
            <!-- БЕЗОПАСНЫЙ ДОСТУП: проверяем, является ли category объектом -->
            <span>{{ typeof problem.category === 'object' ? problem.category?.name : problem.category }}</span>
          </div>
          <div class="info-row">
            <label>Адрес:</label>
            <span><i class="fas fa-location-dot"></i> {{ problem.address }}</span>
          </div>
          <div class="info-row">
            <label>Заявитель:</label>
            <!-- БЕЗОПАСНЫЙ ДОСТУП к author -->
            <span>
              {{ typeof problem.author === 'object' ? problem.author?.full_name : problem.author }}
              <span v-if="typeof problem.author === 'object' && problem.author?.phone">
                ({{ problem.author.phone }})
              </span>
              <span v-else-if="problem.phone">
                ({{ problem.phone }})
              </span>
            </span>
          </div>
          <div class="info-row">
            <label>Дата создания:</label>
            <span>{{ formatDate(problem.created_at) }}</span>
          </div>

          <div class="description-block">
            <label>Описание проблемы:</label>
            <p style="white-space: pre-wrap;">{{ problem.description }}</p>
          </div>

          <div v-if="problem.status === 'rejected' && problem.reject_reason" class="reject-reason">
            <label>Причина отклонения:</label>
            <p class="text-danger">{{ problem.reject_reason }}</p>
          </div>
        </div>

        <!-- Правая колонка: Действия -->
        <div class="actions-section">
          <h3>Действия модератора</h3>

          <!-- Если новое: Одобрить или Отклонить -->
          <div v-if="problem.status === 'new'" class="action-group">
            <button class="btn-action btn-approve" @click="handleApprove" :disabled="isProcessing">
              <i v-if="isProcessing" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-check"></i> Одобрить обращение
            </button>
            <button class="btn-action btn-reject" @click="showRejectForm = true" :disabled="isProcessing">
              <i class="fas fa-ban"></i> Отклонить
            </button>

            <div v-if="showRejectForm" class="reject-form">
              <label>Причина отклонения *</label>
              <textarea v-model="rejectReason" rows="3" placeholder="Укажите причину..."></textarea>
              <div class="form-actions">
                <button class="btn-sm btn-cancel" @click="showRejectForm = false">Отмена</button>
                <button class="btn-sm btn-reject" @click="handleReject" :disabled="!rejectReason.trim() || isProcessing">
                  <span v-if="isProcessing" class="spinner-small"></span>
                  <span v-else>Подтвердить отклонение</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Если одобрено: Назначить исполнителя -->
          <div v-if="problem.status === 'approved'" class="action-group">
            <label>Назначить исполнителя:</label>
            <select v-model="selectedExecutor" class="form-select" :disabled="isProcessing">
              <option value="">Выберите исполнителя...</option>
              <option v-for="exec in executors" :key="exec.id" :value="exec.id">
                {{ exec.full_name }}
              </option>
            </select>
            <button class="btn-action btn-assign" @click="handleAssign" :disabled="!selectedExecutor || isProcessing">
              <span v-if="isProcessing" class="spinner-small"></span>
              <i v-else class="fas fa-user-plus"></i> Назначить и начать работу
            </button>
          </div>

          <!-- Если в работе или решено: Только инфо -->
          <div v-if="['in_progress', 'resolved'].includes(problem.status)" class="action-group info-only">
            <p><i class="fas fa-info-circle"></i> Обращение находится в работе или уже решено. Изменение статуса доступно в панели исполнителя.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps({
  problem: { type: Object, required: true },
  executors: { type: Array, required: true }
})

const emit = defineEmits(['close', 'moderated'])

const problemsStore = useProblemsStore()
const { success, error: showError } = useNotifications()

const showRejectForm = ref(false)
const rejectReason = ref('')
const selectedExecutor = ref('')
const isProcessing = ref(false) // Индикатор загрузки для блокировки кнопок

function getStatusLabel(status) {
  const labels = { new: 'Новое', approved: 'Одобрено', in_progress: 'В работе', resolved: 'Решено', rejected: 'Отклонено' }
  return labels[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function handleApprove() {
  isProcessing.value = true
  try {
    await problemsStore.moderateProblem(props.problem.id, 'approved')
    success('Обращение одобрено')
    emit('moderated')
  } catch {
    showError('Ошибка при одобрении')
  } finally {
    isProcessing.value = false
  }
}

async function handleReject() {
  isProcessing.value = true
  try {
    await problemsStore.moderateProblem(props.problem.id, 'rejected', rejectReason.value)
    success('Обращение отклонено')
    emit('moderated')
  } catch {
    showError('Ошибка при отклонении')
  } finally {
    isProcessing.value = false
  }
}

async function handleAssign() {
  isProcessing.value = true
  try {
    await problemsStore.assignProblem(props.problem.id, selectedExecutor.value)
    success('Исполнитель назначен, статус изменен на "В работе"')
    emit('moderated')
  } catch {
    showError('Ошибка при назначении')
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 800px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); display: flex; flex-direction: column; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; display: grid; grid-template-columns: 1.5fr 1fr; gap: 2rem; }

.info-section { display: flex; flex-direction: column; gap: 1rem; }
.info-row { display: flex; gap: 1rem; font-size: 0.9rem; }
.info-row label { color: #70808c; font-weight: 600; min-width: 120px; }
.status-badge { display: inline-flex; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; }
.status-new { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-in_progress { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-resolved { background: rgba(0, 168, 150, 0.12); color: #00a896; }
.status-rejected { background: rgba(113, 128, 150, 0.12); color: #70808c; }

.description-block, .reject-reason { margin-top: 0.5rem; padding-top: 1rem; border-top: 1px solid #f1f5f9; }
.description-block label, .reject-reason label { display: block; color: #70808c; font-weight: 600; font-size: 0.82rem; margin-bottom: 0.5rem; }
.description-block p { margin: 0; color: #172f40; line-height: 1.6; font-size: 0.95rem; }
.text-danger { color: #c64752; font-weight: 600; }

.actions-section { background: #f8fafc; border-radius: 16px; padding: 1.5rem; border: 1px solid #e8edf0; }
.actions-section h3 { margin: 0 0 1.25rem; font-size: 1rem; font-weight: 800; color: #172f40; }
.action-group { display: flex; flex-direction: column; gap: 0.75rem; }

.btn-action { width: 100%; padding: 0.85rem; border-radius: 12px; border: none; font-size: 0.9rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: all 0.2s ease; }
.btn-approve { background: linear-gradient(135deg, #06d6a0, #05b88a); color: white; box-shadow: 0 4px 12px rgba(6, 214, 160, 0.25); }
.btn-approve:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35); }
.btn-reject { background: linear-gradient(135deg, #c64752, #a83a44); color: white; box-shadow: 0 4px 12px rgba(198, 71, 82, 0.25); }
.btn-reject:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(198, 71, 82, 0.35); }
.btn-assign { background: linear-gradient(135deg, #00a896, #087e8b); color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-assign:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }

.btn-action:disabled { opacity: 0.7; cursor: not-allowed; transform: none !important; }

.reject-form { margin-top: 0.5rem; padding: 1rem; background: white; border-radius: 12px; border: 1px solid #e8edf0; }
.reject-form label { display: block; font-size: 0.82rem; font-weight: 700; color: #172f40; margin-bottom: 0.5rem; }
.reject-form textarea { width: 100%; border: 1px solid #e8edf0; border-radius: 8px; padding: 0.75rem; font-family: inherit; font-size: 0.9rem; resize: vertical; outline: none; }
.reject-form textarea:focus { border-color: #00a896; box-shadow: 0 0 0 3px rgba(0, 168, 150, 0.1); }
.form-actions { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
.btn-sm { flex: 1; padding: 0.6rem; border-radius: 8px; border: none; font-size: 0.82rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-sm.btn-cancel { background: #f1f5f9; color: #172f40; }
.btn-sm.btn-reject { background: #c64752; color: white; }
.btn-sm.btn-reject:disabled { opacity: 0.5; cursor: not-allowed; }

.form-select { width: 100%; padding: 0.75rem; border: 1px solid #e8edf0; border-radius: 10px; background: white; font-size: 0.9rem; color: #172f40; outline: none; margin-bottom: 0.75rem; }
.form-select:focus { border-color: #00a896; }
.form-select:disabled { background: #f1f5f9; cursor: not-allowed; }

.info-only { color: #70808c; font-size: 0.9rem; line-height: 1.5; background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e8edf0; }
.info-only i { color: #0dcaf0; margin-right: 0.5rem; }

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 767.98px) {
  .modal-body { grid-template-columns: 1fr; }
}
</style>