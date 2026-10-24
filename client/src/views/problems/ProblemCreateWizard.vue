<!-- client/src/views/problems/ProblemCreateWizard.vue -->
<template>

    <div class="wizard-container">
      <div class="wizard-card">

        <!-- Заголовок и прогресс -->
        <div class="wizard-header">
          <h2 class="wizard-title">Новое обращение</h2>
          <div class="wizard-progress">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <div class="step-indicator">
              <span class="step-number">{{ step }}</span>
              <span class="step-text">из {{ maxStep }}: {{ currentStepName }}</span>
            </div>
          </div>
        </div>

        <!-- Сообщение об ошибке валидации -->
        <Transition name="fade">
          <div v-if="validationError" class="validation-error-banner">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ validationError }}
          </div>
        </Transition>

        <!-- Контент шагов с анимацией -->
        <Transition name="step-slide" mode="out-in">

          <!-- ШАГ 1: Контакты -->
          <div v-if="step === 1" key="step1" class="wizard-step">
            <h3 class="step-title">Контактные данные</h3>
            <p class="step-subtitle">Чтобы мы могли связаться с вами для уточнения деталей</p>

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

            <div class="toggle-section">
              <label class="custom-toggle">
                <input type="checkbox" v-model="needAddressDetails">
                <span class="toggle-slider"></span>
                <span class="toggle-label">Указать точный адрес</span>
              </label>
            </div>

            <Transition name="fade">
              <div v-if="needAddressDetails" class="address-block">
                <div class="form-grid">
                  <div class="form-group">
                    <label class="form-label">Город</label>
                    <div class="input-wrapper">
                      <span class="input-icon"><IconFa name="city" /></span>
                      <input v-model="form.address.city" type="text" class="form-control-custom" placeholder="Подольск">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Улица</label>
                    <div class="input-wrapper">
                      <span class="input-icon"><IconFa name="road" /></span>
                      <input v-model="form.address.street" type="text" class="form-control-custom" placeholder="ул. Ленина">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="form-label">Дом</label>
                    <div class="input-wrapper">
                      <span class="input-icon"><IconFa name="building" /></span>
                      <input v-model="form.address.house" type="text" class="form-control-custom" placeholder="д. 10">
                    </div>
                  </div>
                </div>
                <button type="button" class="btn-map-toggle" @click="needMap = !needMap">
                  <IconFa :name="needMap ? 'chevron-up' : 'map-location-dot'" class="me-2" />
                  {{ needMap ? 'Скрыть карту' : 'Указать точку на карте' }}
                </button>
                <Transition name="fade">
                  <MapPicker v-if="needMap" v-model="form.address.coords" class="mt-3" />
                </Transition>
              </div>
            </Transition>
          </div>

          <!-- ШАГ 2: Проблема -->
          <div v-else-if="step === 2" key="step2" class="wizard-step">
            <h3 class="step-title">Что случилось?</h3>
            <p class="step-subtitle">Выберите категорию и конкретную проблему</p>

            <!-- Показываем лоадер, если данные еще грузятся -->
            <div v-if="categoriesStore.isLoading" class="text-center py-4">
              <div class="spinner-border text-civic"></div>
              <p class="text-muted mt-2">Загрузка категорий...</p>
            </div>

            <!-- Если данные загрузились, показываем селектор -->
            <IssueSelector v-else v-model="form.problems" :issues="categoriesStore.problems" />
          </div>

          <!-- ШАГ 3: Решения -->
          <div v-else-if="step === 3" key="step3" class="wizard-step">
            <h3 class="step-title">Как это можно решить?</h3>
            <p class="step-subtitle">Предложите варианты решения (необязательно)</p>
            <IssueSelector v-model="form.solutions" :issues="categoriesStore.solutions" />
          </div>

          <!-- ШАГ 4: Детали -->
          <div v-else-if="step === 4" key="step4" class="wizard-step">
            <h3 class="step-title">Дополнительная информация</h3>

            <div class="form-group">
              <label class="form-label">Подробное описание *</label>
              <div class="input-wrapper textarea-wrapper" :class="{ 'is-invalid': localErrors.description }">
                <span class="input-icon textarea-icon"><IconFa name="align-left" /></span>
                <textarea v-model="form.problem_description" class="form-control-custom" rows="5" placeholder="Опишите проблему максимально подробно..." required></textarea>
              </div>
              <div class="char-count">{{ form.problem_description.length }}/2000</div>
            </div>

            <div class="toggle-section">
              <label class="custom-toggle">
                <input type="checkbox" v-model="needVoiceRecord">
                <span class="toggle-slider"></span>
                <span class="toggle-label">Пояснить проблему голосом</span>
              </label>
            </div>
            <Transition name="fade">
              <AudioRecorder v-if="needVoiceRecord" v-model="form.audio_files" class="mb-3" />
            </Transition>

            <div class="toggle-section">
              <label class="custom-toggle">
                <input type="checkbox" v-model="attachDocs">
                <span class="toggle-slider"></span>
                <span class="toggle-label">Прикрепить фото или документы</span>
              </label>
            </div>
            <Transition name="fade">
              <FileUploader v-if="attachDocs" v-model="form.documents" />
            </Transition>
          </div>

          <!-- ШАГ 5: Сводка -->
          <div v-else-if="step === 5" key="step5" class="wizard-step">
            <h3 class="step-title">Проверьте данные</h3>
            <p class="step-subtitle">Убедитесь, что всё указано верно перед отправкой</p>

            <div class="summary-card">
              <div class="summary-row">
                <span class="summary-label"><IconFa name="user" class="me-2" />Заявитель</span>
                <span class="summary-value">{{ summary.fio }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label"><IconFa name="phone" class="me-2" />Телефон</span>
                <span class="summary-value">{{ summary.phone }}</span>
              </div>
              <div class="summary-row" v-if="summary.address !== 'Не указано'">
                <span class="summary-label"><IconFa name="map-pin" class="me-2" />Адрес</span>
                <span class="summary-value">{{ summary.address }}</span>
              </div>
              <div class="summary-divider"></div>
              <div class="summary-row">
                <span class="summary-label"><IconFa name="circle-info" class="me-2" />Описание</span>
              </div>
              <div class="summary-description">
                {{ form.problem_description || 'Не указано' }}
              </div>

              <div v-if="form.documents.length > 0 || form.audio_files.length > 0" class="summary-divider"></div>
              <div class="summary-row" v-if="form.documents.length > 0">
                <span class="summary-label"><IconFa name="paperclip" class="me-2" />Файлы</span>
                <span class="summary-value">{{ form.documents.length }} шт.</span>
              </div>
              <div class="summary-row" v-if="form.audio_files.length > 0">
                <span class="summary-label"><IconFa name="microphone" class="me-2" />Аудио</span>
                <span class="summary-value">{{ form.audio_files.length }} записей</span>
              </div>
            </div>
          </div>

        </Transition>

        <!-- Навигация -->
        <div class="wizard-navigation">
          <button v-if="step > 1" type="button" @click="prevStep" class="btn-nav btn-nav-secondary">
            <IconFa name="arrow-left" class="me-2" /> Назад
          </button>

          <button v-if="step < 5" type="button" @click="nextStep" class="btn-nav btn-nav-primary">
            Далее <IconFa name="arrow-right" class="ms-2" />
          </button>

          <button v-if="step === 5" type="button" @click="submitForm" :disabled="submitting" class="btn-nav btn-nav-primary btn-nav-submit">
            <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
            <IconFa v-else name="paper-plane" class="me-2" />
            {{ submitting ? 'Отправка...' : 'Отправить обращение' }}
          </button>
        </div>

      </div>
    </div>

</template>

<script>
import AppLayout from '@/layouts/AppLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'
import IssueSelector from '@/components/reports/IssueSelector.vue'
import MapPicker from '@/components/reports/MapPicker.vue'
import FileUploader from '@/components/reports/FileUploader.vue'
import AudioRecorder from '@/components/reports/AudioRecorder.vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useAuthStore } from '@/stores/auth.store'
import { useCategoriesStore } from '@/stores/issue-categories.store'

export default {
  name: 'ProblemCreateWizard',
  components: { AppLayout, IconFa, IssueSelector, MapPicker, FileUploader, AudioRecorder },
  data() {
    return {
      step: 1,
      maxStep: 5,
      submitting: false,
      validationError: '',
      localErrors: {},
      needAddressDetails: false,
      needMap: false,
      needVoiceRecord: false,
      attachDocs: false,
      form: {
        fio: { last: '', first: '', middle: '' },
        phone: '',
        address: { city: '', street: '', house: '', coords: { lat: 55.43, lon: 37.54 } },
        problems: {},
        solutions: {},
        problem_description: '',
        audio_files: [],
        documents: []
      }
    }
  },
  computed: {
    authStore() { return useAuthStore() },
    problemsStore() { return useProblemsStore() },
    categoriesStore() { return useCategoriesStore() },

    progressPercentage() {
      return (this.step / this.maxStep) * 100
    },
    currentStepName() {
      const names = ['', 'Контакты', 'Проблема', 'Решения', 'Детали', 'Проверка']
      return names[this.step]
    },
    summary() {
      const fio = [this.form.fio.last, this.form.fio.first, this.form.fio.middle].filter(Boolean).join(' ')
      const address = [this.form.address.city, this.form.address.street, this.form.address.house].filter(Boolean).join(', ')
      return {
        fio: fio || 'Не указано',
        phone: this.form.phone || 'Не указано',
        address: address || 'Не указано'
      }
    }
  },
  async mounted() {
    // Загружаем справочник категорий с бэкенда
    await this.categoriesStore.fetchCategories()

    // Автозаполнение из профиля
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

    validateStep() {
      this.validationError = ''
      this.localErrors = {}
      let isValid = true

      if (this.step === 1) {
        if (!this.form.fio.first.trim() || !this.form.fio.last.trim()) {
          this.localErrors.fio_first = true
          this.localErrors.fio_last = true
          this.validationError = 'Пожалуйста, укажите Имя и Фамилию'
          isValid = false
        }
        if (this.form.phone.length < 18) {
          this.localErrors.phone = true
          this.validationError = 'Введите корректный номер телефона'
          isValid = false
        }
      }

      if (this.step === 4) {
        if (!this.form.problem_description.trim() || this.form.problem_description.trim().length < 10) {
          this.localErrors.description = true
          this.validationError = 'Опишите проблему подробнее (минимум 10 символов)'
          isValid = false
        }
      }

      return isValid
    },

    nextStep() {
      if (this.validateStep()) {
        this.step++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },

    prevStep() {
      this.validationError = ''
      this.localErrors = {}
      this.step--
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    async submitForm() {
      this.submitting = true
      this.validationError = ''
      try {
        // Имитация API запроса
        await new Promise(resolve => setTimeout(resolve, 1500))

        // В реальности:
        // const formData = new FormData()
        // ... сборка данных
        // await this.problemsStore.createProblem(formData)

        this.$router.push('/problems')
      } catch (error) {
        console.error('Ошибка отправки:', error)
        this.validationError = 'Произошла ошибка при отправке. Попробуйте позже.'
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
/* === Дизайн-система === */
.wizard-container {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;

  padding: 2rem 1rem;
  display: flex;
  justify-content: center;
}

.wizard-card {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.06);
  display: flex;
  flex-direction: column;
  min-height: 600px;
}

/* === Заголовок и прогресс === */
.wizard-header {
  margin-bottom: 2rem;
}

.wizard-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--layout-ink);
  letter-spacing: -0.03em;
  margin: 0 0 1.5rem;
  text-align: center;
}

.wizard-progress {
  position: relative;
}

.progress-track {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00a896, #087e8b);
  border-radius: 3px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  font-size: 0.88rem;
  color: var(--layout-muted);
  font-weight: 600;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: var(--layout-accent);
  color: white;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 800;
}

/* === Ошибки === */
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

/* === Шаги === */
.wizard-step {
  flex: 1;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 0.25rem;
}

.step-subtitle {
  color: var(--layout-muted);
  font-size: 0.9rem;
  margin: 0 0 1.5rem;
}

/* === Формы === */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 576px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.form-group {
  margin-bottom: 0.5rem;
}

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

.textarea-icon {
  align-items: flex-start;
  padding-top: 0.85rem;
}

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

.form-control-custom:focus {
  outline: none;
  box-shadow: none;
}

.form-control-custom::placeholder {
  color: #aab5bc;
}

.textarea-wrapper {
  align-items: flex-start;
}

.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: var(--layout-muted);
  margin-top: 0.35rem;
}

/* === Переключатели === */
.toggle-section {
  margin: 1.5rem 0 1rem;
}

.custom-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 0.75rem;
}

.custom-toggle input {
  display: none;
}

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

.custom-toggle input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 0.95rem;
  font-weight: 650;
  color: var(--layout-ink);
}

/* === Карта === */
.btn-map-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  border: 1px dashed var(--layout-line);
  border-radius: 12px;
  background: transparent;
  color: var(--layout-accent);
  font-weight: 650;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-map-toggle:hover {
  background: rgba(0, 168, 150, 0.05);
  border-color: var(--layout-accent);
}

/* === Сводка === */
.summary-card {
  background: #f8fafc;
  border: 1px solid var(--layout-line);
  border-radius: 16px;
  padding: 1.5rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.summary-label {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--layout-muted);
  display: flex;
  align-items: center;
}

.summary-value {
  font-size: 0.95rem;
  font-weight: 650;
  color: var(--layout-ink);
  text-align: right;
  max-width: 60%;
}

.summary-divider {
  height: 1px;
  background: var(--layout-line);
  margin: 1rem 0;
}

.summary-description {
  font-size: 0.95rem;
  color: var(--layout-ink);
  line-height: 1.6;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid var(--layout-line);
}

/* === Навигация === */
.wizard-navigation {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--layout-line);
}

.btn-nav {
  flex: 1;
  padding: 0.95rem;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 750;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

.btn-nav-secondary {
  background: #f1f5f9;
  color: var(--layout-ink);
}

.btn-nav-secondary:hover {
  background: #e2e8f0;
}

.btn-nav-primary {
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
}

.btn-nav-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
}

.btn-nav-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* === Анимации === */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.step-slide-enter-active {
  transition: all 0.3s ease-out;
}
.step-slide-leave-active {
  transition: all 0.2s ease-in;
  position: absolute;
  width: 100%;
}
.step-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.step-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .wizard-container {
    padding: 1rem 0.5rem;
  }
  .wizard-card {
    padding: 1.5rem 1.25rem;
    border-radius: 20px;
    min-height: auto;
  }
  .wizard-title {
    font-size: 1.5rem;
  }
  .wizard-navigation {
    flex-direction: column-reverse;
  }
  .btn-nav {
    width: 100%;
  }
}
</style>