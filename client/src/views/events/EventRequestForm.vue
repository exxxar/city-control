<!-- client/src/views/events/EventRequestForm.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="page-header-modern">
        <div>
          <h2 class="page-title">Заявка на мероприятие</h2>
          <p class="page-subtitle">Заполните форму, чтобы организовать событие в вашем городе</p>
        </div>
      </div>
    </template>

    <div class="form-container">
      <form @submit.prevent="submitForm" class="modern-form">

        <!-- Сообщение об ошибке валидации -->
        <Transition name="fade">
          <div v-if="validationError" class="validation-error-banner">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ validationError }}
          </div>
        </Transition>

        <!-- Секция 1: Контактные данные -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="user-group" class="me-2" /> Организатор
          </h3>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Фамилия *</label>
              <div class="input-wrapper" :class="{ 'is-invalid': localErrors.fio_last }">
                <span class="input-icon"><IconFa name="user" /></span>
                <input v-model="form.fio.last" type="text" class="form-control-custom" placeholder="Иванов" required>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Имя *</label>
              <div class="input-wrapper" :class="{ 'is-invalid': localErrors.fio_first }">
                <span class="input-icon"><IconFa name="user" /></span>
                <input v-model="form.fio.first" type="text" class="form-control-custom" placeholder="Иван" required>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Отчество</label>
              <div class="input-wrapper">
                <span class="input-icon"><IconFa name="user" /></span>
                <input v-model="form.fio.middle" type="text" class="form-control-custom" placeholder="Иванович">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Телефон *</label>
              <div class="input-wrapper" :class="{ 'is-invalid': localErrors.phone }">
                <span class="input-icon"><IconFa name="phone" /></span>
                <input :value="form.phone" @input="formatPhone" type="tel" class="form-control-custom" placeholder="+7 (___) ___-__-__" required>
              </div>
            </div>
          </div>
        </div>

        <!-- Секция 2: Детали мероприятия -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="calendar-star" class="me-2" /> Детали события
          </h3>

          <div class="form-group">
            <label class="form-label">Муниципалитет *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.municipality }">
              <span class="input-icon"><IconFa name="building" /></span>
              <select v-model="form.municipality_id" class="form-control-custom form-select-custom" required>
                <option value="" disabled>Выберите муниципалитет</option>
                <option v-for="m in municipalities" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Дата мероприятия *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': localErrors.event_date }">
              <span class="input-icon"><IconFa name="calendar-days" /></span>
              <input v-model="form.event_date" type="date" class="form-control-custom" required>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Описание (цели, программа) *</label>
            <div class="input-wrapper textarea-wrapper" :class="{ 'is-invalid': localErrors.description }">
              <span class="input-icon textarea-icon"><IconFa name="align-left" /></span>
              <textarea v-model="form.description" class="form-control-custom" rows="4" placeholder="Опишите, что планируется..." required minlength="20"></textarea>
            </div>
            <div class="char-count">{{ form.description.length }}/2000</div>
          </div>

          <div class="form-group">
            <label class="form-label">Целевая аудитория</label>
            <div class="input-wrapper">
              <span class="input-icon"><IconFa name="users" /></span>
              <input v-model="form.target_audience" type="text" class="form-control-custom" placeholder="Например: жители района, семьи с детьми">
            </div>
          </div>

          <!-- Счетчик участников -->
          <div class="form-group">
            <label class="form-label">Ожидаемое количество участников</label>
            <div class="participants-stepper">
              <button type="button" class="stepper-btn" @click="decrease">
                <IconFa name="minus" />
              </button>
              <div class="stepper-display" @click="toggleInput">
                <span v-if="!showInput">{{ form.participants_count }}</span>
                <input v-else v-model.number="form.participants_count" type="number" min="0" class="stepper-input" autofocus @blur="showInput = false">
                <span class="stepper-label">чел.</span>
              </div>
              <button type="button" class="stepper-btn" @click="increase">
                <IconFa name="plus" />
              </button>
            </div>
          </div>
        </div>

        <!-- Секция 3: Дополнительные потребности -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="hand-holding-heart" class="me-2" /> Поддержка и материалы
          </h3>

          <div class="toggle-section">
            <label class="custom-toggle">
              <input type="checkbox" v-model="needHelp">
              <span class="toggle-slider"></span>
              <span class="toggle-label">Нужна помощь администрации/организаторов</span>
            </label>
          </div>

          <Transition name="fade">
            <div v-if="needHelp" class="nested-form-block">
              <label class="form-label small">Форматы необходимой помощи</label>

              <!-- Показываем лоадер -->
              <div v-if="helpFormatsStore.isLoading" class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-civic"></div>
                <span class="ms-2 text-muted">Загрузка форматов...</span>
              </div>

              <!-- Если данные загрузились -->
              <template v-else>
                <div v-for="(item, index) in form.help_formats" :key="index" class="input-group-custom mb-2">
                  <div class="input-wrapper flex-grow-1">
                    <select v-model="form.help_formats[index]" class="form-control-custom form-select-custom">
                      <option value="" disabled>Выберите формат</option>
                      <option v-for="hf in availableHelpFormats(index)" :key="hf.id" :value="hf.id">
                        {{ hf.name }}
                      </option>
                    </select>
                  </div>
                  <button type="button" class="btn-remove" @click="removeHelpFormat(index)">
                    <IconFa name="times" />
                  </button>
                </div>
                <button type="button" class="btn-add-format" @click="addHelpFormat" :disabled="!hasAvailableHelpFormats">
                  <IconFa name="plus" class="me-1" /> Добавить формат помощи
                </button>
              </template>
            </div>
          </Transition>

          <div class="toggle-section">
            <label class="custom-toggle">
              <input type="checkbox" v-model="attachDocs">
              <span class="toggle-slider"></span>
              <span class="toggle-label">Прикрепить документы или смету</span>
            </label>
          </div>
          <Transition name="fade">
            <FileUploader v-if="attachDocs" v-model="form.documents" class="mt-2" />
          </Transition>

          <div class="toggle-section">
            <label class="custom-toggle">
              <input type="checkbox" v-model="needVoiceRecord">
              <span class="toggle-slider"></span>
              <span class="toggle-label">Пояснить детали голосом</span>
            </label>
          </div>
          <Transition name="fade">
            <AudioRecorder v-if="needVoiceRecord" v-model="form.audio_files" class="mt-2" />
          </Transition>
        </div>

        <!-- Кнопка отправки -->
        <div class="form-actions">
          <button type="submit" class="btn-submit-primary" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            <IconFa v-else name="paper-plane" class="me-2" />
            {{ isSubmitting ? 'Отправка заявки...' : 'Отправить заявку' }}
          </button>
        </div>

      </form>
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import FileUploader from '@/components/reports/FileUploader.vue'
import AudioRecorder from '@/components/reports/AudioRecorder.vue'
import { useEventsStore } from '@/stores/events.store'
import { useAuthStore } from '@/stores/auth.store'
import { useHelpFormatsStore } from '@/stores/helpFormats.store'

export default {
  name: 'EventRequestForm',
  components: { AppPageContainer, IconFa, FileUploader, AudioRecorder },
  data() {
    return {
      isSubmitting: false,
      validationError: '',
      localErrors: {},
      needVoiceRecord: false,
      needHelp: false,
      attachDocs: false,
      showInput: false,
      form: {
        fio: { last: '', first: '', middle: '' },
        phone: '',
        municipality_id: '',
        event_date: '',
        description: '',
        target_audience: '',
        participants_count: 10,
        help_formats: [],
        documents: [],
        audio_files: []
      },
      municipalities: [
        { id: 1, name: 'г. Подольск' },
        { id: 2, name: 'г. Климовск' },
        { id: 3, name: 'п. Львовский' }
      ]
    }
  },
  computed: {
    authStore() { return useAuthStore() },
    eventsStore() { return useEventsStore() },
    helpFormatsStore() { return useHelpFormatsStore() },
    hasAvailableHelpFormats() {
      const selectedCount = this.form.help_formats.filter(id => id !== '').length
      return this.helpFormatsStore.items.length > selectedCount
    }
  },
  async mounted() {
    // Загружаем форматы помощи с бэкенда
    await this.helpFormatsStore.fetchHelpFormats()

    this.loadForm()
    const today = new Date()
    this.form.event_date = today.toISOString().split('T')[0]

    if (this.authStore.user?.full_name) {
      const names = this.authStore.user.full_name.split(' ')
      this.form.fio.last = names[0] || ''
      this.form.fio.first = names[1] || ''
      this.form.fio.middle = names[2] || ''
    }
  },
  methods: {
    formatPhone(e) {
      let val = e.target.value.replace(/\D/g, '')
      if (val.length > 0) {
        if (val[0] === '7' || val[0] === '8') val = val.substring(1)
        let formatted = '+7'
        if (val.length > 0) formatted += ' (' + val.substring(0, 3)
        if (val.length >= 3) formatted += ') ' + val.substring(3, 6)
        if (val.length >= 6) formatted += '-' + val.substring(6, 8)
        if (val.length >= 8) formatted += '-' + val.substring(8, 10)
        this.form.phone = formatted
      } else {
        this.form.phone = ''
      }
    },

    saveForm() {
      localStorage.setItem('event_form_fio', JSON.stringify(this.form.fio))
      localStorage.setItem('event_form_phone', this.form.phone)
      localStorage.setItem('event_form_municipality', this.form.municipality_id)
    },

    loadForm() {
      const fio = localStorage.getItem('event_form_fio')
      const phone = localStorage.getItem('event_form_phone')
      const municipality = localStorage.getItem('event_form_municipality')
      if (fio) this.form.fio = JSON.parse(fio)
      if (phone) this.form.phone = phone
      if (municipality) this.form.municipality_id = municipality
    },

    increase() { this.form.participants_count++ },
    decrease() { if (this.form.participants_count > 0) this.form.participants_count-- },
    toggleInput() { this.showInput = !this.showInput },

    addHelpFormat() {
      if (this.hasAvailableHelpFormats) this.form.help_formats.push('')
    },
    removeHelpFormat(index) {
      this.form.help_formats.splice(index, 1)
    },
    availableHelpFormats(index) {
      const selectedIds = this.form.help_formats.filter((id, i) => i !== index && id !== '')
      return this.helpFormatsStore.items.filter(hf => !selectedIds.includes(hf.id))
    },

    validateForm() {
      this.validationError = ''
      this.localErrors = {}
      let isValid = true

      if (!this.form.fio.first.trim() || !this.form.fio.last.trim()) {
        this.localErrors.fio_first = true
        this.localErrors.fio_last = true
        this.validationError = 'Пожалуйста, укажите Имя и Фамилию организатора'
        isValid = false
      }
      if (this.form.phone.length < 18) {
        this.localErrors.phone = true
        this.validationError = 'Введите корректный номер телефона'
        isValid = false
      }
      if (!this.form.municipality_id) {
        this.localErrors.municipality = true
        this.validationError = 'Выберите муниципалитет'
        isValid = false
      }
      if (!this.form.description.trim() || this.form.description.trim().length < 20) {
        this.localErrors.description = true
        this.validationError = 'Опишите мероприятие подробнее (минимум 20 символов)'
        isValid = false
      }

      return isValid
    },

    async submitForm() {
      if (!this.validateForm()) return

      this.isSubmitting = true
      this.saveForm()

      try {
        const formData = new FormData()
        formData.append('fio', `${this.form.fio.last} ${this.form.fio.first} ${this.form.fio.middle}`.trim())
        formData.append('phone', this.form.phone)
        formData.append('municipality_id', this.form.municipality_id)
        formData.append('event_date', this.form.event_date)
        formData.append('description', this.form.description)
        formData.append('target_audience', this.form.target_audience)
        formData.append('participants_count', this.form.participants_count)
        formData.append('help_formats', JSON.stringify(this.form.help_formats.filter(id => id !== '')))

        this.form.documents.forEach((file, i) => formData.append(`documents[${i}]`, file))
        this.form.audio_files.forEach((file, i) => formData.append(`audio_files[${i}]`, file))

        await this.eventsStore.createEvent(formData)

        localStorage.removeItem('event_form_fio')
        localStorage.removeItem('event_form_phone')
        localStorage.removeItem('event_form_municipality')

        this.$router.push('/events')
      } catch (error) {
        console.error('Ошибка отправки заявки:', error)
        this.validationError = error.response?.data?.detail || 'Произошла ошибка при отправке заявки. Попробуйте позже.'
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

/* === Счетчик участников === */
.participants-stepper {
  display: flex;
  align-items: center;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: #fcfcfd;
  overflow: hidden;
  width: fit-content;
}
.stepper-btn {
  width: 48px;
  height: 48px;
  border: none;
  background: transparent;
  color: var(--layout-ink);
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stepper-btn:hover { background: #e2e8f0; }
.stepper-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--layout-ink);
  cursor: pointer;
  min-width: 120px;
  justify-content: center;
}
.stepper-input {
  width: 60px;
  border: none;
  background: transparent;
  font-size: 1.1rem;
  font-weight: 700;
  text-align: center;
  color: var(--layout-ink);
}
.stepper-input:focus { outline: none; }
.stepper-label { font-size: 0.85rem; font-weight: 500; color: var(--layout-muted); }

/* === Переключатели и вложенные блоки === */
.toggle-section { margin: 1.5rem 0 1rem; }
.custom-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 0.75rem;
}
.custom-toggle input { display: none; }
.toggle-slider {
  width: 44px;
  height: 24px;
  background: #cbd5e1;
  border-radius: 12px;
  position: relative;
  transition: 0.3s;
  flex-shrink: 0;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  top: 3px;
  left: 3px;
  transition: 0.3s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.custom-toggle input:checked + .toggle-slider {
  background: linear-gradient(135deg, #00a896, #087e8b);
}
.custom-toggle input:checked + .toggle-slider::before { transform: translateX(20px); }
.toggle-label { font-size: 0.95rem; font-weight: 650; color: var(--layout-ink); }

.nested-form-block {
  background: #f8fafc;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  padding: 1.25rem;
  margin-top: 0.5rem;
}

.input-group-custom { display: flex; gap: 0.5rem; }
.btn-remove {
  width: 48px;
  height: 48px;
  border: 1px solid #fecaca;
  border-radius: 14px;
  background: #fef2f2;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.btn-remove:hover { background: #fee2e2; }

.btn-add-format {
  width: 100%;
  padding: 0.75rem;
  border: 1px dashed var(--layout-accent);
  border-radius: 12px;
  background: transparent;
  color: var(--layout-accent);
  font-weight: 650;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}
.btn-add-format:hover:not(:disabled) { background: rgba(0, 168, 150, 0.05); }
.btn-add-format:disabled { opacity: 0.5; cursor: not-allowed; }

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
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, max-height 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 575.98px) {
  .modern-form { padding: 1.5rem 1.25rem; border-radius: 16px; }
  .page-title { font-size: 1.5rem; }
}
</style>