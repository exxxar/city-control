<!-- admin/src/components/reports/ReportDetailModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Отчёт #{{ report.id }}</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <div class="modal-body">
        <!-- Основная информация -->
        <div class="info-section">
          <div class="info-row">
            <label>Статус:</label>
            <span class="status-badge" :class="`status-${report.status}`">{{ getStatusLabel(report.status) }}</span>
          </div>
          <div class="info-row">
            <label>Проблема:</label>
            <span>{{ report.problem_title }} (#{{ report.problem_id }})</span>
          </div>
          <div class="info-row">
            <label>Исполнитель:</label>
            <span>{{ report.executor_name }}</span>
          </div>
          <div class="info-row">
            <label>Дата выполнения:</label>
            <span>{{ formatDate(report.work_date) }}</span>
          </div>
          <div class="info-row">
            <label>Отчёт отправлен:</label>
            <span>{{ formatDateTime(report.submitted_at) }}</span>
          </div>
          <div class="info-row">
            <label>Стоимость работ:</label>
            <span class="cost-value">{{ report.cost.toLocaleString('ru-RU') }} ₽</span>
          </div>

          <div class="description-block">
            <label>Описание выполненных работ:</label>
            <p>{{ report.work_description || 'Не указано' }}</p>
          </div>

          <div v-if="report.materials_used" class="materials-block">
            <label>Использованные материалы:</label>
            <p>{{ report.materials_used }}</p>
          </div>

          <!-- Фото до/после -->
          <div class="photos-section">
            <div class="photos-group">
              <label>Фото ДО ({{ report.photos_before }} шт.)</label>
              <div class="photos-grid">
                <div v-for="i in report.photos_before" :key="'before-' + i" class="photo-placeholder photo-before">
                  <i class="fas fa-image"></i>
                  <span>Фото {{ i }}</span>
                </div>
                <div v-if="report.photos_before === 0" class="no-photos">Нет фото</div>
              </div>
            </div>

            <div class="photos-group">
              <label>Фото ПОСЛЕ ({{ report.photos_after }} шт.)</label>
              <div class="photos-grid">
                <div v-for="i in report.photos_after" :key="'after-' + i" class="photo-placeholder photo-after">
                  <i class="fas fa-image"></i>
                  <span>Фото {{ i }}</span>
                </div>
                <div v-if="report.photos_after === 0" class="no-photos">Нет фото</div>
              </div>
            </div>
          </div>

          <!-- Причина отклонения -->
          <div v-if="report.status === 'rejected' && report.reject_reason" class="reject-reason-block">
            <label><i class="fas fa-circle-xmark"></i> Причина отклонения:</label>
            <p>{{ report.reject_reason }}</p>
          </div>

          <!-- Комментарий к доработке -->
          <div v-if="report.status === 'revision' && report.revision_comment" class="revision-block">
            <label><i class="fas fa-redo"></i> Комментарий к доработке:</label>
            <p>{{ report.revision_comment }}</p>
          </div>
        </div>

        <!-- Действия -->
        <div class="actions-section" v-if="report.status === 'pending' || report.status === 'revision'">
          <h3>Проверка отчёта</h3>

          <button class="btn-action btn-approve" @click="handleApprove">
            <i class="fas fa-check-circle"></i> Принять отчёт
          </button>

          <button class="btn-action btn-revision" @click="showRevisionForm = true">
            <i class="fas fa-redo"></i> Вернуть на доработку
          </button>

          <button class="btn-action btn-reject" @click="showRejectForm = true">
            <i class="fas fa-times-circle"></i> Отклонить отчёт
          </button>

          <!-- Форма доработки -->
          <div v-if="showRevisionForm" class="action-form">
            <label>Комментарий для исполнителя *</label>
            <textarea v-model="revisionComment" rows="3" placeholder="Укажите, что нужно доработать..."></textarea>
            <div class="form-actions">
              <button class="btn-sm btn-cancel" @click="showRevisionForm = false">Отмена</button>
              <button class="btn-sm btn-revision" @click="handleRevision" :disabled="!revisionComment.trim()">Отправить на доработку</button>
            </div>
          </div>

          <!-- Форма отклонения -->
          <div v-if="showRejectForm" class="action-form">
            <label>Причина отклонения *</label>
            <textarea v-model="rejectReason" rows="3" placeholder="Укажите причину отклонения..."></textarea>
            <div class="form-actions">
              <button class="btn-sm btn-cancel" @click="showRejectForm = false">Отмена</button>
              <button class="btn-sm btn-reject" @click="handleReject" :disabled="!rejectReason.trim()">Отклонить</button>
            </div>
          </div>
        </div>

        <!-- Только просмотр для принятых/отклонённых -->
        <div v-else class="actions-section info-only">
          <p><i class="fas fa-info-circle"></i> Отчёт уже обработан. Изменение статуса невозможно.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useReportsStore } from '@/stores/reports.store'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps({
  report: { type: Object, required: true }
})

const emit = defineEmits(['close', 'approved', 'rejected', 'revision'])

const reportsStore = useReportsStore()
const { success, error: showError } = useNotifications()

const showRevisionForm = ref(false)
const showRejectForm = ref(false)
const revisionComment = ref('')
const rejectReason = ref('')

function getStatusLabel(status) {
  const labels = {
    pending: 'На проверке',
    approved: 'Принят',
    rejected: 'Отклонён',
    revision: 'На доработке'
  }
  return labels[status] || status
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function formatDateTime(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('ru-RU', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
}

async function handleApprove() {
  try {
    await reportsStore.approveReport(props.report.id)
    success('Отчёт принят, проблема закрыта')
    emit('approved')
  } catch {
    showError('Ошибка при принятии отчёта')
  }
}

async function handleRevision() {
  try {
    await reportsStore.requestRevision(props.report.id, revisionComment.value)
    success('Отчёт возвращён на доработку')
    emit('revision')
  } catch {
    showError('Ошибка при возврате на доработку')
  }
}

async function handleReject() {
  try {
    await reportsStore.rejectReport(props.report.id, rejectReason.value)
    success('Отчёт отклонён')
    emit('rejected')
  } catch {
    showError('Ошибка при отклонении отчёта')
  }
}
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 850px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; display: grid; grid-template-columns: 1.5fr 1fr; gap: 2rem; }

.info-section { display: flex; flex-direction: column; gap: 1rem; }
.info-row { display: flex; gap: 1rem; font-size: 0.9rem; }
.info-row label { color: #70808c; font-weight: 600; min-width: 140px; }
.cost-value { font-weight: 700; color: #00a896; }

.status-badge { display: inline-flex; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; }
.status-pending { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
.status-approved { background: rgba(6, 214, 160, 0.12); color: #06d6a0; }
.status-rejected { background: rgba(198, 71, 82, 0.12); color: #c64752; }
.status-revision { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }

.description-block, .materials-block, .reject-reason-block, .revision-block { margin-top: 0.5rem; padding-top: 1rem; border-top: 1px solid #f1f5f9; }
.description-block label, .materials-block label, .reject-reason-block label, .revision-block label { display: block; color: #70808c; font-weight: 600; font-size: 0.82rem; margin-bottom: 0.5rem; }
.description-block p, .materials-block p { margin: 0; color: #172f40; line-height: 1.6; font-size: 0.95rem; }
.reject-reason-block p { margin: 0; color: #c64752; font-weight: 600; line-height: 1.5; }
.revision-block p { margin: 0; color: #0dcaf0; font-weight: 600; line-height: 1.5; }
.reject-reason-block i, .revision-block i { margin-right: 0.5rem; }

.photos-section { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #f1f5f9; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.photos-group label { display: block; color: #70808c; font-weight: 600; font-size: 0.82rem; margin-bottom: 0.75rem; }
.photos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 0.5rem; }
.photo-placeholder { aspect-ratio: 1; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; font-size: 0.7rem; gap: 0.25rem; border: 2px solid; }
.photo-placeholder i { font-size: 1.25rem; }
.photo-before { background: rgba(198, 71, 82, 0.15); border-color: #c64752; }
.photo-after { background: rgba(6, 214, 160, 0.15); border-color: #06d6a0; }
.no-photos { color: #70808c; font-size: 0.85rem; font-style: italic; padding: 1rem; text-align: center; background: #f8fafc; border-radius: 8px; }

.actions-section { background: #f8fafc; border-radius: 16px; padding: 1.5rem; border: 1px solid #e8edf0; }
.actions-section h3 { margin: 0 0 1.25rem; font-size: 1rem; font-weight: 800; color: #172f40; }
.btn-action { width: 100%; padding: 0.85rem; border-radius: 12px; border: none; font-size: 0.9rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: all 0.2s ease; margin-bottom: 0.75rem; }
.btn-approve { background: linear-gradient(135deg, #06d6a0, #05b88a); color: white; box-shadow: 0 4px 12px rgba(6, 214, 160, 0.25); }
.btn-approve:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35); }
.btn-revision { background: linear-gradient(135deg, #0dcaf0, #0aa2c0); color: white; box-shadow: 0 4px 12px rgba(13, 202, 240, 0.25); }
.btn-revision:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(13, 202, 240, 0.35); }
.btn-reject { background: linear-gradient(135deg, #c64752, #a83a44); color: white; box-shadow: 0 4px 12px rgba(198, 71, 82, 0.25); }
.btn-reject:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(198, 71, 82, 0.35); }

.action-form { margin-top: 1rem; padding: 1rem; background: white; border-radius: 12px; border: 1px solid #e8edf0; }
.action-form label { display: block; font-size: 0.82rem; font-weight: 700; color: #172f40; margin-bottom: 0.5rem; }
.action-form textarea { width: 100%; border: 1px solid #e8edf0; border-radius: 8px; padding: 0.75rem; font-family: inherit; font-size: 0.9rem; resize: vertical; outline: none; }
.action-form textarea:focus { border-color: #00a896; box-shadow: 0 0 0 3px rgba(0, 168, 150, 0.1); }
.form-actions { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
.btn-sm { flex: 1; padding: 0.6rem; border-radius: 8px; border: none; font-size: 0.82rem; font-weight: 700; cursor: pointer; }
.btn-sm.btn-cancel { background: #f1f5f9; color: #172f40; }
.btn-sm.btn-revision { background: #0dcaf0; color: white; }
.btn-sm.btn-reject { background: #c64752; color: white; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }

.info-only { color: #70808c; font-size: 0.9rem; line-height: 1.5; background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e8edf0; }
.info-only i { color: #0dcaf0; margin-right: 0.5rem; }

@media (max-width: 767.98px) {
  .modal-body { grid-template-columns: 1fr; }
  .photos-section { grid-template-columns: 1fr; }
}
</style>