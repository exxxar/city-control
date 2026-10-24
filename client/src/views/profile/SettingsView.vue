<!-- client/src/views/profile/SettingsView.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="page-header-modern">
        <div>
          <h2 class="page-title">Настройки</h2>
          <p class="page-subtitle">Управляйте уведомлениями, приватностью и геолокацией</p>
        </div>
      </div>
    </template>

    <div class="settings-grid">

      <!-- Уведомления -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-icon-wrapper settings-icon--blue">
            <IconFa name="bell" size="1.25rem" />
          </div>
          <div>
            <h3 class="settings-card-title">Уведомления</h3>
            <p class="settings-card-subtitle">Контролируйте, как мы с вами связываемся</p>
          </div>
        </div>

        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Push-уведомления</div>
              <div class="setting-description">Мгновенные уведомления в браузере</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.push_notifications">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Email-уведомления</div>
              <div class="setting-description">Письма о статусе обращений</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.email_notifications">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Гео-уведомления</div>
              <div class="setting-description">О проблемах рядом с вами</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.geo_notifications">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Приватность -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-icon-wrapper settings-icon--purple">
            <IconFa name="shield-halved" size="1.25rem" />
          </div>
          <div>
            <h3 class="settings-card-title">Приватность</h3>
            <p class="settings-card-subtitle">Защита ваших данных на фотографиях</p>
          </div>
        </div>

        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Размывать лица</div>
              <div class="setting-description">Автоматически скрывать лица на фото</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.auto_blur_faces">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Размывать номера авто</div>
              <div class="setting-description">Скрывать номера автомобилей</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.auto_blur_plates">
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Удалять метаданные</div>
              <div class="setting-description">Очищать EXIF-данные из фото</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.remove_exif">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Геолокация -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-icon-wrapper settings-icon--green">
            <IconFa name="location-dot" size="1.25rem" />
          </div>
          <div>
            <h3 class="settings-card-title">Геолокация</h3>
            <p class="settings-card-subtitle">Для карт и AR-режима</p>
          </div>
        </div>

        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">Включить геолокацию</div>
              <div class="setting-description">Необходимо для гео-уведомлений и AR</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.location_enabled">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Кнопка сохранения и уведомление -->
      <div class="settings-actions">
        <Transition name="fade">
          <div v-if="saveSuccess" class="save-notification save-notification--success">
            <IconFa name="circle-check" class="me-2" />
            Настройки успешно сохранены
          </div>
        </Transition>

        <Transition name="fade">
          <div v-if="saveError" class="save-notification save-notification--error">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ saveError }}
          </div>
        </Transition>

        <button
            class="btn-save-modern"
            @click="saveSettings"
            :disabled="isSaving"
        >
          <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
          {{ isSaving ? 'Сохранение...' : 'Сохранить настройки' }}
        </button>
      </div>

    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import { storageService } from '@/services/storage.service'

export default {
  name: 'SettingsView',
  components: { AppPageContainer, IconFa },
  data() {
    return {
      settings: {
        push_notifications: true,
        email_notifications: true,
        geo_notifications: true,
        auto_blur_faces: true,
        auto_blur_plates: true,
        remove_exif: true,
        location_enabled: true
      },
      isSaving: false,
      saveSuccess: false,
      saveError: ''
    }
  },
  mounted() {
    this.loadSettings()
  },
  methods: {
    loadSettings() {
      const saved = storageService.getLocal('user_settings')
      if (saved) {
        this.settings = { ...this.settings, ...saved }
      }
    },

    async saveSettings() {
      this.isSaving = true
      this.saveSuccess = false
      this.saveError = ''

      try {
        storageService.setLocal('user_settings', this.settings)
        this.saveSuccess = true

        // Автоматически скрываем уведомление через 3 секунды
        setTimeout(() => {
          this.saveSuccess = false
        }, 3000)
      } catch (error) {
        console.error('Save settings error:', error)
        this.saveError = 'Ошибка сохранения. Попробуйте позже.'
      } finally {
        this.isSaving = false
      }
    }
  }
}
</script>

<style scoped>
/* === Переменные дизайн-системы === */
.settings-grid {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;

  max-width: 800px;
  margin: 0 auto;
}

/* === Заголовок страницы === */
.page-header-modern {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--layout-ink);
  letter-spacing: -0.03em;
  margin: 0;
}

.page-subtitle {
  color: var(--layout-muted);
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

/* === Карточки настроек === */
.settings-card {
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 20px;
  padding: 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
  transition: box-shadow 0.2s ease;
}

.settings-card:hover {
  box-shadow: 0 8px 30px rgba(23, 47, 64, 0.08);
}

.settings-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--layout-line);
}

.settings-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  flex-shrink: 0;
}

.settings-icon--blue {
  background: rgba(13, 202, 240, 0.1);
  color: #0dcaf0;
}

.settings-icon--purple {
  background: rgba(111, 66, 193, 0.1);
  color: #6f42c1;
}

.settings-icon--green {
  background: rgba(0, 168, 150, 0.1);
  color: #00a896;
}

.settings-card-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 0.25rem;
  letter-spacing: -0.02em;
}

.settings-card-subtitle {
  color: var(--layout-muted);
  font-size: 0.88rem;
  margin: 0;
}

/* === Список настроек === */
.settings-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
}

.setting-info {
  flex: 1;
  min-width: 0;
}

.setting-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--layout-ink);
  margin-bottom: 0.25rem;
}

.setting-description {
  font-size: 0.82rem;
  color: var(--layout-muted);
  line-height: 1.4;
}

/* === Toggle Switch (Современный) === */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 28px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
  transition: 0.3s;
  border-radius: 28px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.toggle-switch input:checked + .toggle-slider {
  background: linear-gradient(135deg, #00a896, #087e8b);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.toggle-switch input:focus + .toggle-slider {
  box-shadow: 0 0 0 3px rgba(0, 168, 150, 0.2);
}

/* === Действия (кнопка сохранения) === */
.settings-actions {
  margin-top: 2rem;
}

.btn-save-modern {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-size: 1rem;
  font-weight: 750;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.25);
}

.btn-save-modern:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 168, 150, 0.35);
}

.btn-save-modern:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* === Уведомления === */
.save-notification {
  display: flex;
  align-items: center;
  padding: 0.85rem 1rem;
  margin-bottom: 1rem;
  border-radius: 12px;
  font-size: 0.88rem;
  font-weight: 600;
}

.save-notification--success {
  background: rgba(6, 214, 160, 0.1);
  border: 1px solid rgba(6, 214, 160, 0.3);
  color: #059669;
}

.save-notification--error {
  background: #fff0f1;
  border: 1px solid rgba(198, 71, 82, 0.2);
  color: #c64752;
}

/* === Анимации === */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .settings-card {
    padding: 1.25rem;
    border-radius: 16px;
  }

  .settings-card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .toggle-switch {
    align-self: flex-end;
  }

  .page-title {
    font-size: 1.5rem;
  }
}
</style>