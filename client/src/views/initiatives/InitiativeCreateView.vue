<!-- client/src/views/initiatives/InitiativeCreateView.vue -->
<template>
  <div class="form-page-container">
    <!-- Современный заголовок -->
    <div class="page-header-modern">
      <div>
        <h2 class="page-title">
          <IconFa name="lightbulb" class="me-2 text-civic" />
          Предложить инициативу
        </h2>
        <p class="page-subtitle">Поделитесь своей идеей по улучшению города</p>
      </div>
    </div>

    <div class="form-container">
      <form @submit.prevent="submitInitiative" class="modern-form">

        <!-- Баннер ошибки -->
        <Transition name="fade">
          <div v-if="validationError || submitError" class="validation-error-banner">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ validationError || submitError }}
          </div>
        </Transition>

        <!-- Секция 1: Основная информация -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="circle-info" class="me-2" /> Основная информация
          </h3>

          <div class="form-group">
            <label class="form-label">Название инициативы *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.title }">
              <span class="input-icon"><IconFa name="heading" /></span>
              <input
                  v-model="form.title"
                  type="text"
                  class="form-control-custom"
                  placeholder="Например: Установить новую детскую площадку"
                  maxlength="255"
                  required
              >
            </div>
            <div v-if="localErrors.title" class="error-message">{{ localErrors.title }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">Подробное описание *</label>
            <div class="input-wrapper textarea-wrapper" :class="{ 'is-invalid': localErrors.description }">
              <span class="input-icon textarea-icon"><IconFa name="align-left" /></span>
              <textarea
                  v-model="form.description"
                  class="form-control-custom"
                  rows="5"
                  placeholder="Опишите вашу идею, её цели и ожидаемую пользу для жителей..."
                  maxlength="2000"
                  required
              ></textarea>
            </div>
            <div class="char-count">{{ form.description.length }}/2000</div>
            <div v-if="localErrors.description" class="error-message">{{ localErrors.description }}</div>
          </div>
        </div>

        <!-- Секция 2: Детали и медиа -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="map-location-dot" class="me-2" /> Детали и материалы
          </h3>

          <div class="form-group">
            <label class="form-label">Территория</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.territory_id }">
              <span class="input-icon"><IconFa name="map" /></span>
              <select v-model="form.territory_id" class="form-control-custom form-select-custom">
                <option value="">Выберите территорию (необязательно)</option>
                <option v-for="terr in territories" :key="terr.id" :value="terr.id">
                  {{ terr.name }}
                </option>
              </select>
            </div>
            <div v-if="localErrors.territory_id" class="error-message">{{ localErrors.territory_id }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">Фотографии или документы</label>
            <p class="text-muted small mb-2">Прикрепите эскизы, фотографии места или другие материалы</p>
            <MediaUploader
                :multiple="true"
                :max-files="5"
                @files-selected="onFilesSelected"
            />
          </div>
        </div>

        <!-- Кнопка отправки -->
        <div class="form-actions">
          <button type="submit" class="btn-submit-primary" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            <IconFa v-else name="paper-plane" class="me-2" />
            {{ isSubmitting ? 'Отправка инициативы...' : 'Отправить инициативу' }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import MediaUploader from '@/components/media/MediaUploader.vue'
import { useInitiativesStore } from '@/stores/initiatives.store'
import * as mapsApi from '@/api/maps.api'

export default {
  name: 'InitiativeCreateView',
  components: { IconFa, MediaUploader },
  data() {
    return {
      form: {
        title: '',
        description: '',
        territory_id: ''
      },
      territories: [],
      files: [],
      localErrors: {},
      validationError: '',
      submitError: '',
      isSubmitting: false
    }
  },
  async mounted() {
    await this.loadTerritories()
  },
  methods: {
    async loadTerritories() {
      try {
        const response = await mapsApi.getTerritories()
        this.territories = response.data || response || []
      } catch (error) {
        console.error('Failed to load territories:', error)
      }
    },

    onFilesSelected(files) {
      this.files = files
    },

    validateForm() {
      this.localErrors = {}
      this.validationError = ''
      let isValid = true

      if (!this.form.title.trim()) {
        this.localErrors.title = 'Введите название инициативы'
        isValid = false
      }
      if (!this.form.description.trim()) {
        this.localErrors.description = 'Введите описание инициативы'
        isValid = false
      }

      if (!isValid) {
        this.validationError = 'Пожалуйста, проверьте правильность заполнения выделенных полей'
      }

      return isValid
    },

    async submitInitiative() {
      if (!this.validateForm()) return

      this.isSubmitting = true
      this.submitError = ''
      this.validationError = ''

      try {
        const initiativesStore = useInitiativesStore()

        // Подготовка данных (в реальном проекте здесь может быть FormData)
        const payload = {
          ...this.form,
          // Если territory_id пустая строка, превращаем в null
          territory_id: this.form.territory_id || null
        }

        await initiativesStore.createInitiative(payload)

        this.$router.push('/initiatives')
      } catch (error) {
        console.error('Create initiative error:', error)
        this.submitError = error.response?.data?.detail || 'Ошибка создания инициативы. Попробуйте позже.'
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
/* === Дизайн-система === */
.form-page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header-modern {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0;
  display: flex;
  align-items: center;
}

.text-civic {
  color: #00a896;
}

.page-subtitle {
  color: #70808c;
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

.form-container {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;
}

.modern-form {
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 2.5rem;
  border-bottom: 1px solid var(--layout-line);
}
.form-section:last-of-type { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }

.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 1.25rem;
  display: flex;
  align-items: center;
}

/* === Инпуты === */
.form-group { margin-bottom: 1rem; }
.form-label {
  display: block;
  margin-bottom: 0.45rem;
  color: var(--layout-ink);
  font-size: 0.88rem;
  font-weight: 700;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: #fcfcfd;
  transition: all 180ms ease;
  overflow: hidden;
}
.input-wrapper:focus-within {
  border-color: var(--layout-accent);
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
}
.input-wrapper.is-invalid {
  border-color: #c64752;
  background: #fff0f1;
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  flex-shrink: 0;
  color: var(--layout-muted);
}
.textarea-icon { align-items: flex-start; padding-top: 0.85rem; }

.form-control-custom {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.85rem 1rem 0.85rem 0;
  color: var(--layout-ink);
  font-size: 0.95rem;
  width: 100%;
  resize: vertical;
}
.form-control-custom:focus { outline: none; box-shadow: none; }
.form-control-custom::placeholder { color: #aab5bc; }

.form-select-custom {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%2370808c' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px 12px;
  padding-right: 2.5rem;
}

.textarea-wrapper { align-items: flex-start; }
.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: var(--layout-muted);
  margin-top: 0.35rem;
}
.error-message {
  margin-top: 0.4rem;
  color: #c64752;
  font-size: 0.82rem;
  font-weight: 600;
}

/* === Ошибки и действия === */
.validation-error-banner {
  display: flex;
  align-items: center;
  padding: 0.85rem 1rem;
  margin-bottom: 1.5rem;
  border-radius: 12px;
  background: #fff0f1;
  border: 1px solid rgba(198, 71, 82, 0.2);
  color: #c64752;
  font-size: 0.88rem;
  font-weight: 600;
}

.form-actions { margin-top: 2rem; }
.btn-submit-primary {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-size: 1rem;
  font-weight: 750;
  cursor: pointer;
  transition: all 180ms ease;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-submit-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 168, 150, 0.35);
}
.btn-submit-primary:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

/* === Анимации === */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .form-page-container { padding: 1.5rem 1rem; }
  .modern-form { padding: 1.5rem 1.25rem; border-radius: 16px; }
  .page-title { font-size: 1.5rem; }
}
</style>