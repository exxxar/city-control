<!-- client/src/views/events/EventCreateView.vue -->
<template>


    <div class="form-container">
      <form @submit.prevent="submitEvent" class="modern-form">

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
            <label class="form-label">Название мероприятия *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.title }">
              <span class="input-icon"><IconFa name="heading" /></span>
              <input
                  v-model="form.title"
                  type="text"
                  class="form-control-custom"
                  placeholder="Например: Субботник в центральном парке"
                  maxlength="255"
                  required
              >
            </div>
            <div v-if="localErrors.title" class="error-message">{{ localErrors.title }}</div>
          </div>

          <div class="form-group">
            <label class="form-label">Тип мероприятия *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.event_type }">
              <span class="input-icon"><IconFa name="tag" /></span>
              <select v-model="form.event_type" class="form-control-custom form-select-custom" required>
                <option value="" disabled>Выберите тип</option>
                <option value="subbotnik">Субботник</option>
                <option value="meeting">Собрание граждан</option>
                <option value="exhibition">Выставка</option>
                <option value="concert">Концерт</option>
                <option value="fair">Ярмарка</option>
                <option value="action">Общественная акция</option>
                <option value="other">Другое</option>
              </select>
            </div>
            <div v-if="localErrors.event_type" class="error-message">{{ localErrors.event_type }}</div>
          </div>
        </div>

        <!-- Секция 2: Время и место -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="calendar-days" class="me-2" /> Время и место
          </h3>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Дата и время начала *</label>
              <div class="input-wrapper" :class="{ 'is-invalid': localErrors.start_date }">
                <span class="input-icon"><IconFa name="clock" /></span>
                <input v-model="form.start_date" type="datetime-local" class="form-control-custom" required>
              </div>
              <div v-if="localErrors.start_date" class="error-message">{{ localErrors.start_date }}</div>
            </div>
            <div class="form-group">
              <label class="form-label">Дата и время окончания</label>
              <div class="input-wrapper" :class="{ 'is-invalid': localErrors.end_date }">
                <span class="input-icon"><IconFa name="clock" /></span>
                <input v-model="form.end_date" type="datetime-local" class="form-control-custom">
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Место проведения *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.location_text }">
              <span class="input-icon"><IconFa name="map-location-dot" /></span>
              <input
                  v-model="form.location_text"
                  type="text"
                  class="form-control-custom"
                  placeholder="Адрес или описание места (например: Парк культуры, у главного входа)"
                  required
              >
            </div>
            <div v-if="localErrors.location_text" class="error-message">{{ localErrors.location_text }}</div>
          </div>
        </div>

        <!-- Секция 3: Детали и медиа -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="users" class="me-2" /> Детали и материалы
          </h3>

          <div class="form-group">
            <label class="form-label">Ожидаемое количество участников</label>
            <div class="input-wrapper">
              <span class="input-icon"><IconFa name="users" /></span>
              <input
                  v-model="form.expected_participants"
                  type="number"
                  class="form-control-custom"
                  placeholder="Например: 50"
                  min="1"
              >
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Описание мероприятия</label>
            <div class="input-wrapper textarea-wrapper">
              <span class="input-icon textarea-icon"><IconFa name="align-left" /></span>
              <textarea
                  v-model="form.description"
                  class="form-control-custom"
                  rows="5"
                  placeholder="Расскажите о целях, программе, необходимых ресурсах..."
                  maxlength="2000"
              ></textarea>
            </div>
            <div class="char-count">{{ form.description.length }}/2000</div>
          </div>

          <div class="form-group">
            <label class="form-label">Фотографии или документы</label>
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
            {{ isSubmitting ? 'Отправка заявки...' : 'Подать заявку' }}
          </button>
        </div>

      </form>
    </div>

</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import MediaUploader from '@/components/media/MediaUploader.vue'
import { useEventsStore } from '@/stores/events.store'

export default {
  name: 'EventCreateView',
  components: { AppPageContainer, IconFa, MediaUploader },
  data() {
    return {
      form: {
        title: '',
        event_type: '',
        start_date: '',
        end_date: '',
        location_text: '',
        expected_participants: '',
        description: ''
      },
      files: [],
      localErrors: {},
      validationError: '',
      submitError: '',
      isSubmitting: false
    }
  },
  methods: {
    validateForm() {
      this.localErrors = {}
      this.validationError = ''
      let isValid = true

      if (!this.form.title.trim()) {
        this.localErrors.title = 'Введите название мероприятия'
        isValid = false
      }
      if (!this.form.event_type) {
        this.localErrors.event_type = 'Выберите тип мероприятия'
        isValid = false
      }
      if (!this.form.start_date) {
        this.localErrors.start_date = 'Укажите дату и время начала'
        isValid = false
      } else if (new Date(this.form.start_date) < new Date()) {
        this.localErrors.start_date = 'Дата начала не может быть в прошлом'
        isValid = false
      }
      if (!this.form.location_text.trim()) {
        this.localErrors.location_text = 'Укажите место проведения'
        isValid = false
      }

      if (!isValid) {
        this.validationError = 'Пожалуйста, проверьте правильность заполнения выделенных полей'
      }

      return isValid
    },

    onFilesSelected(files) {
      this.files = files
    },

    async submitEvent() {
      if (!this.validateForm()) return

      this.isSubmitting = true
      this.submitError = ''
      this.validationError = ''

      try {
        const eventsStore = useEventsStore()

        // Подготовка данных (в реальном проекте здесь может быть FormData, если MediaUploader возвращает File объекты)
        const payload = {
          ...this.form,
          start_date: new Date(this.form.start_date).toISOString(),
          end_date: this.form.end_date ? new Date(this.form.end_date).toISOString() : null,
          expected_participants: this.form.expected_participants ? parseInt(this.form.expected_participants) : null
        }

        await eventsStore.createEvent(payload)

        // Перенаправляем на список мероприятий или в профиль
        this.$router.push('/events')
      } catch (error) {
        console.error('Create event error:', error)
        this.submitError = error.response?.data?.detail || 'Ошибка подачи заявки. Попробуйте позже.'
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
/* === Дизайн-система === */
.form-container {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;

  max-width: 750px;
  margin: 0 auto;
}

.page-header-modern { margin-bottom: 1.5rem; }
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

/* === Сетка и инпуты === */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
@media (min-width: 576px) {
  .form-grid { grid-template-columns: 1fr 1fr; }
}

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
  .modern-form { padding: 1.5rem 1.25rem; border-radius: 16px; }
  .page-title { font-size: 1.5rem; }
}
</style>