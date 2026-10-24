<!-- admin/src/views/settings/SettingsView.vue -->
<template>
  <div class="settings-page">
    <!-- Заголовок -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Настройки системы</h1>
        <p class="page-subtitle">Управление глобальными параметрами приложения</p>
      </div>
      <button class="btn-save-top" @click="saveAll" :disabled="!hasChanges || settingsStore.isSaving">
        <span v-if="settingsStore.isSaving" class="spinner-small"></span>
        <i v-else class="fas fa-save"></i>
        {{ settingsStore.isSaving ? 'Сохранение...' : 'Сохранить все изменения' }}
      </button>
    </div>

    <!-- Уведомление о моковых данных -->
    <Transition name="fade">
      <div v-if="settingsStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные. API настроек на бэкенде пока не настроен.</span>
      </div>
    </Transition>

    <!-- Уведомление об изменениях -->
    <Transition name="fade">
      <div v-if="hasChanges" class="changes-notice">
        <i class="fas fa-exclamation-triangle"></i>
        <span>Есть несохранённые изменения. Нажмите "Сохранить все изменения" вверху страницы.</span>
      </div>
    </Transition>

    <!-- Загрузка -->
    <div v-if="settingsStore.isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка настроек...</p>
    </div>

    <!-- Контент -->
    <div v-else-if="settingsStore.settings" class="settings-content">
      <!-- Табы -->
      <div class="tabs-container">
        <div class="tabs">
          <button
              v-for="tab in tabs"
              :key="tab.value"
              class="tab-btn"
              :class="{ active: activeTab === tab.value }"
              @click="activeTab = tab.value"
          >
            <i :class="tab.icon"></i>
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Контент табов -->
      <div class="tab-content">
        <!-- Общие настройки -->
        <div v-if="activeTab === 'general'" class="settings-section">
          <h2 class="section-title">
            <i class="fas fa-building"></i>
            Организация
          </h2>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Название организации</label>
              <input v-model="form.organization_name" type="text" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Email организации</label>
              <input v-model="form.organization_email" type="email" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Телефон организации</label>
              <input v-model="form.organization_phone" type="tel" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Адрес организации</label>
              <input v-model="form.organization_address" type="text" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Email технической поддержки</label>
              <input v-model="form.support_email" type="email" class="form-control-custom">
            </div>
          </div>
        </div>

        <!-- Настройки модерации -->
        <div v-if="activeTab === 'moderation'" class="settings-section">
          <h2 class="section-title">
            <i class="fas fa-shield-halved"></i>
            Модерация
          </h2>

          <div class="toggle-group">
            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Автоматическое одобрение от доверенных пользователей</div>
                <div class="toggle-desc">Обращения от проверенных пользователей будут одобряться без модерации</div>
              </div>
              <input type="checkbox" v-model="form.auto_approve_trusted_users" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>

            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Требовать фото для обращений</div>
                <div class="toggle-desc">Пользователи обязаны прикрепить хотя бы одно фото к обращению</div>
              </div>
              <input type="checkbox" v-model="form.require_photos_for_problems" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Минимальная длина описания (символов)</label>
              <input v-model.number="form.min_description_length" type="number" min="0" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Максимум фото на одно обращение</label>
              <input v-model.number="form.max_photos_per_problem" type="number" min="1" max="20" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Максимальный размер фото (МБ)</label>
              <input v-model.number="form.max_photo_size_mb" type="number" min="1" max="50" class="form-control-custom">
            </div>
          </div>
        </div>

        <!-- Настройки уведомлений -->
        <div v-if="activeTab === 'notifications'" class="settings-section">
          <h2 class="section-title">
            <i class="fas fa-bell"></i>
            Уведомления
          </h2>

          <div class="toggle-group">
            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Email-уведомления</div>
                <div class="toggle-desc">Отправлять уведомления на электронную почту</div>
              </div>
              <input type="checkbox" v-model="form.email_notifications_enabled" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>

            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Push-уведомления</div>
                <div class="toggle-desc">Отправлять push-уведомления в браузер</div>
              </div>
              <input type="checkbox" v-model="form.push_notifications_enabled" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>

            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Уведомлять о новых обращениях</div>
                <div class="toggle-desc">Администраторы получат уведомление при создании нового обращения</div>
              </div>
              <input type="checkbox" v-model="form.notify_on_new_problem" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>

            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Уведомлять об изменении статуса</div>
                <div class="toggle-desc">Пользователи получат уведомление при изменении статуса их обращения</div>
              </div>
              <input type="checkbox" v-model="form.notify_on_status_change" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>

            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Уведомлять исполнителя при назначении</div>
                <div class="toggle-desc">Исполнитель получит уведомление, когда ему назначат новое обращение</div>
              </div>
              <input type="checkbox" v-model="form.notify_executor_on_assign" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <!-- Лимиты -->
        <div v-if="activeTab === 'limits'" class="settings-section">
          <h2 class="section-title">
            <i class="fas fa-gauge-high"></i>
            Лимиты и ограничения
          </h2>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Максимум обращений в день (на пользователя)</label>
              <input v-model.number="form.max_problems_per_day" type="number" min="1" class="form-control-custom">
              <small class="form-hint">Защита от спама</small>
            </div>

            <div class="form-group">
              <label class="form-label">Максимум инициатив в месяц</label>
              <input v-model.number="form.max_initiatives_per_month" type="number" min="1" class="form-control-custom">
            </div>

            <div class="form-group">
              <label class="form-label">Максимум мероприятий в месяц</label>
              <input v-model.number="form.max_events_per_month" type="number" min="1" class="form-control-custom">
            </div>
          </div>

          <div class="toggle-group">
            <label class="toggle-item">
              <div class="toggle-info">
                <div class="toggle-title">Требовать подтверждение email при регистрации</div>
                <div class="toggle-desc">Новые пользователи должны подтвердить свой email перед входом</div>
              </div>
              <input type="checkbox" v-model="form.registration_requires_email_verification" class="toggle-input">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Модалка подтверждения сохранения -->
    <ConfirmModal
        v-if="showConfirmSave"
        title="Сохранение настроек"
        message="Вы уверены, что хотите сохранить все изменения? Некоторые настройки могут повлиять на работу системы."
        confirm-text="Сохранить"
        confirm-class="btn-primary"
        @confirm="confirmSave"
        @cancel="showConfirmSave = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useSettingsStore } from '@/stores/settings.store'
import { useNotifications } from '@/composables/useNotifications'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'

const settingsStore = useSettingsStore()
const { success, error: showError } = useNotifications()

const activeTab = ref('general')
const showConfirmSave = ref(false)

const tabs = [
  { value: 'general', label: 'Общие', icon: 'fas fa-building' },
  { value: 'moderation', label: 'Модерация', icon: 'fas fa-shield-halved' },
  { value: 'notifications', label: 'Уведомления', icon: 'fas fa-bell' },
  { value: 'limits', label: 'Лимиты', icon: 'fas fa-gauge-high' }
]

const form = reactive({})
const originalForm = ref({})

// Инициализация формы из store
watch(() => settingsStore.settings, (newSettings) => {
  if (newSettings) {
    Object.assign(form, newSettings)
    originalForm.value = { ...newSettings }
  }
}, { immediate: true })

// Проверка наличия изменений
const hasChanges = computed(() => {
  return JSON.stringify(form) !== JSON.stringify(originalForm.value)
})

function saveAll() {
  showConfirmSave.value = true
}

async function confirmSave() {
  try {
    await settingsStore.updateSettings({ ...form })
    originalForm.value = { ...form }
    success('Настройки успешно сохранены')
    showConfirmSave.value = false
  } catch (error) {
    showError('Ошибка при сохранении настроек')
  }
}

onMounted(async () => {
  await settingsStore.fetchSettings()
})
</script>

<style scoped lang="scss">
.settings-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

.btn-save-top { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #00a896, #087e8b); color: white; border: none; border-radius: 12px; font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-save-top:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }
.btn-save-top:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.spinner-small { width: 16px; height: 16px; border: 2px solid rgba(255, 255, 255, 0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.changes-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: rgba(253, 126, 20, 0.1); border: 1px solid rgba(253, 126, 20, 0.3); border-radius: 12px; color: #fd7e14; font-size: 0.88rem; font-weight: 600; }

.loading-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 400px; color: #70808c; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }

.tabs-container { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 0.5rem; }
.tabs { display: flex; gap: 0.5rem; overflow-x: auto; }
.tab-btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; border: none; background: transparent; color: #70808c; font-size: 0.9rem; font-weight: 600; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; white-space: nowrap; }
.tab-btn:hover { background: #f1f5f9; color: #172f40; }
.tab-btn.active { background: linear-gradient(135deg, #00a896, #087e8b); color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }

.tab-content { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 2rem; }

.settings-section { max-width: 800px; }
.section-title { display: flex; align-items: center; gap: 0.75rem; margin: 0 0 1.5rem; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.section-title i { color: #00a896; font-size: 1.1rem; }

.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }
.form-group { display: flex; flex-direction: column; }
.form-label { display: block; margin-bottom: 0.45rem; color: #172f40; font-size: 0.88rem; font-weight: 700; }
.form-control-custom { width: 100%; border: 1px solid #e8edf0; border-radius: 12px; background: #fcfcfd; padding: 0.75rem 1rem; color: #172f40; font-size: 0.9rem; outline: none; transition: all 180ms ease; }
.form-control-custom:focus { border-color: #00a896; background: white; box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1); }
.form-hint { display: block; margin-top: 0.35rem; color: #70808c; font-size: 0.78rem; }

.toggle-group { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
.toggle-item { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1rem; background: #f8fafc; border: 1px solid #e8edf0; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; }
.toggle-item:hover { background: #f1f5f9; border-color: #00a896; }
.toggle-info { flex: 1; }
.toggle-title { font-weight: 700; color: #172f40; font-size: 0.95rem; margin-bottom: 0.25rem; }
.toggle-desc { color: #70808c; font-size: 0.82rem; line-height: 1.4; }

.toggle-input { display: none; }
.toggle-slider { position: relative; width: 48px; height: 26px; background: #cbd5e1; border-radius: 13px; transition: 0.3s; flex-shrink: 0; }
.toggle-slider::before { content: ''; position: absolute; width: 20px; height: 20px; border-radius: 50%; background: white; top: 3px; left: 3px; transition: 0.3s; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.toggle-input:checked + .toggle-slider { background: linear-gradient(135deg, #00a896, #087e8b); }
.toggle-input:checked + .toggle-slider::before { transform: translateX(22px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 767.98px) {
  .form-grid { grid-template-columns: 1fr; }
  .tabs { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 0.5rem; }
  .toggle-item { flex-direction: column; align-items: flex-start; }
}
</style>