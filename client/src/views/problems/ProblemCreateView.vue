<!-- client/src/views/problems/ProblemCreateView.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="page-header-modern">
        <div>
          <h2 class="page-title">Сообщить о проблеме</h2>
          <p class="page-subtitle">Заполните форму, чтобы мы могли оперативно решить вопрос</p>
        </div>
      </div>
    </template>

    <div class="form-container">
      <form @submit.prevent="submitProblem" class="modern-form">

        <!-- Секция 1: Основная информация -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="circle-info" class="me-2" /> Основная информация
          </h3>

          <!-- Категория -->
          <div class="form-group">
            <label for="category" class="form-label">Категория проблемы *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': errors.category_id }">
              <span class="input-icon">
                <IconFa name="tags" />
              </span>
              <select
                  id="category"
                  v-model="form.category_id"
                  class="form-control-custom form-select-custom"
                  required
              >
                <option value="" disabled>Выберите категорию</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
            <div v-if="errors.category_id" class="error-message">{{ errors.category_id }}</div>
          </div>

          <!-- Заголовок -->
          <div class="form-group">
            <label for="title" class="form-label">Краткий заголовок *</label>
            <div class="input-wrapper" :class="{ 'is-invalid': errors.title }">
              <span class="input-icon">
                <IconFa name="heading" />
              </span>
              <input
                  id="title"
                  v-model="form.title"
                  type="text"
                  class="form-control-custom"
                  placeholder="Например: Яма на дороге"
                  maxlength="255"
                  required
              >
            </div>
            <div v-if="errors.title" class="error-message">{{ errors.title }}</div>
          </div>

          <!-- Описание -->
          <div class="form-group">
            <label for="description" class="form-label">Подробное описание *</label>
            <div class="input-wrapper textarea-wrapper" :class="{ 'is-invalid': errors.description }">
              <span class="input-icon textarea-icon">
                <IconFa name="align-left" />
              </span>
              <textarea
                  id="description"
                  v-model="form.description"
                  class="form-control-custom"
                  placeholder="Опишите проблему подробнее: где именно, как давно, какие есть риски..."
                  rows="5"
                  maxlength="2000"
                  required
              ></textarea>
            </div>
            <div class="char-count">{{ form.description.length }}/2000</div>
            <div v-if="errors.description" class="error-message">{{ errors.description }}</div>
          </div>
        </div>

        <!-- Секция 2: Медиа -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="camera" class="me-2" /> Фото и видео
          </h3>
          <p class="section-subtitle">Прикрепите фотографии или видео, чтобы мы лучше поняли ситуацию</p>
          <MediaUploader
              :multiple="true"
              :max-files="10"
              @files-selected="onFilesSelected"
          />
        </div>

        <!-- Секция 3: Локация -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="location-dot" class="me-2" /> Местоположение
          </h3>
          <div class="form-group">
            <label class="form-label">Адрес или координаты</label>
            <div class="location-input-group">
              <div class="input-wrapper flex-grow-1" :class="{ 'is-invalid': errors.location }">
                <span class="input-icon">
                  <IconFa name="map-pin" />
                </span>
                <input
                    type="text"
                    class="form-control-custom"
                    :value="locationText || 'Определяется...'"
                    readonly
                    placeholder="Координаты не определены"
                >
              </div>
              <button type="button" class="btn-action-icon" @click="openMapPicker" title="Выбрать на карте">
                <IconFa name="map" />
              </button>
              <button type="button" class="btn-action-icon" @click="detectLocation" title="Определить автоматически">
                <IconFa name="crosshairs" />
              </button>
            </div>
            <small class="text-muted d-block mt-2">
              <IconFa name="info-circle" class="me-1" />
              Координаты определяются автоматически при загрузке или выбираются вручную на карте.
            </small>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="form-actions">
          <button type="submit" class="btn-submit-primary" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            <IconFa v-else name="paper-plane" class="me-2" />
            {{ isSubmitting ? 'Отправка...' : 'Отправить обращение' }}
          </button>

          <button type="button" class="btn-submit-secondary" @click="saveToOfflineQueue">
            <IconFa name="cloud-arrow-up" class="me-2" />
            Сохранить черновик (offline)
          </button>
        </div>

        <!-- Глобальная ошибка формы -->
        <div v-if="errors.form" class="error-message text-center mt-3">
          {{ errors.form }}
        </div>

      </form>
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import MediaUploader from '@/components/media/MediaUploader.vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useOfflineQueue } from '@/composables/useOfflineQueue'
import * as categoriesApi from '@/api/categories.api'

export default {
  name: 'ProblemCreateView',
  components: {
    AppPageContainer,
    IconFa,
    MediaUploader
  },
  data() {
    return {
      form: {
        category_id: '',
        title: '',
        description: '',
        latitude: null,
        longitude: null,
        territory_id: null,
        geo_tag_id: null
      },
      files: [],
      categories: [],
      errors: {},
      isSubmitting: false,
      locationText: ''
    }
  },
  async mounted() {
    await this.loadCategories()
    this.detectLocation()
  },
  methods: {
    async loadCategories() {
      try {
        const response = await categoriesApi.getCategories()
        this.categories = response.data || response || []
      } catch (error) {
        console.error('Failed to load categories:', error)
        // Fallback данные, если API временно недоступен
        this.categories = [
          { id: 1, name: 'Дороги и транспорт' },
          { id: 2, name: 'ЖКХ и благоустройство' },
          { id: 3, name: 'Безопасность и правопорядок' }
        ]
      }
    },

    detectLocation() {
      this.locationText = 'Определяем местоположение...'
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
              this.form.latitude = position.coords.latitude
              this.form.longitude = position.coords.longitude
              this.locationText = `${this.form.latitude.toFixed(5)}, ${this.form.longitude.toFixed(5)}`
            },
            (error) => {
              console.warn('Geolocation error:', error)
              this.locationText = 'Не удалось определить. Укажите вручную.'
            }
        )
      } else {
        this.locationText = 'Геолокация не поддерживается браузером'
      }
    },

    onFilesSelected(files) {
      this.files = files
    },

    openMapPicker() {
      // TODO: Открыть модальное окно с картой для выбора точки
      // Временная заглушка для демонстрации
      if (!this.form.latitude) {
        this.form.latitude = 55.4315
        this.form.longitude = 37.5460
      }
      this.locationText = `${this.form.latitude.toFixed(5)}, ${this.form.longitude.toFixed(5)} (выбрано на карте)`
    },

    async submitProblem() {
      this.errors = {}

      if (!this.form.category_id) {
        this.errors.category_id = 'Выберите категорию'
        return
      }
      if (!this.form.title.trim()) {
        this.errors.title = 'Введите заголовок'
        return
      }
      if (!this.form.description.trim() || this.form.description.trim().length < 10) {
        this.errors.description = 'Описание должно содержать минимум 10 символов'
        return
      }

      this.isSubmitting = true
      try {
        const problemsStore = useProblemsStore()
        const problem = await problemsStore.createProblem(this.form)

        // TODO: Загрузить файлы через files.api
        if (this.files.length > 0) {
          console.log('Files to upload:', this.files)
        }

        this.$router.push({ name: 'ProblemDetails', params: { id: problem.id } })
      } catch (error) {
        console.error('Failed to create problem:', error)
        this.errors.form = error.response?.data?.detail || 'Ошибка создания обращения. Попробуйте позже.'
      } finally {
        this.isSubmitting = false
      }
    },

    saveToOfflineQueue() {
      try {
        const { addProblemToQueue } = useOfflineQueue()
        addProblemToQueue({ ...this.form, files: this.files })
        alert('Обращение сохранено в очередь и будет отправлено при восстановлении связи')
        this.$router.push('/')
      } catch (error) {
        console.error('Offline queue error:', error)
        alert('Ошибка сохранения в офлайн-очередь')
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

  max-width: 700px;
  margin: 0 auto;
}

.page-header-modern {
  margin-bottom: 1.5rem;
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

/* === Карточка формы === */
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

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 0.5rem;
  display: flex;
  align-items: center;
}

.section-subtitle {
  color: var(--layout-muted);
  font-size: 0.88rem;
  margin: 0 0 1.25rem;
}

/* === Поля ввода === */
.form-group {
  margin-bottom: 1.25rem;
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
  transition: color 180ms ease;
}

.textarea-icon {
  align-items: flex-start;
  padding-top: 0.85rem;
}

.input-wrapper:focus-within .input-icon {
  color: var(--layout-accent);
}

.input-wrapper.is-invalid .input-icon {
  color: #c64752;
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

.form-select-custom {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%2370808c' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px 12px;
  padding-right: 2.5rem;
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

.error-message {
  margin-top: 0.4rem;
  color: #c64752;
  font-size: 0.82rem;
  font-weight: 600;
}

/* === Локация === */
.location-input-group {
  display: flex;
  gap: 0.75rem;
}

.btn-action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: #fcfcfd;
  color: var(--layout-muted);
  cursor: pointer;
  transition: all 180ms ease;
  flex-shrink: 0;
}

.btn-action-icon:hover {
  border-color: var(--layout-accent);
  background: rgba(0, 168, 150, 0.05);
  color: var(--layout-accent);
}

/* === Кнопки действий === */
.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

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

.btn-submit-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-submit-secondary {
  width: 100%;
  padding: 0.85rem;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: transparent;
  color: var(--layout-ink);
  font-size: 0.95rem;
  font-weight: 650;
  cursor: pointer;
  transition: all 180ms ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-submit-secondary:hover {
  border-color: var(--layout-accent);
  background: rgba(0, 168, 150, 0.04);
  color: var(--layout-accent);
}

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .modern-form {
    padding: 1.5rem 1.25rem;
    border-radius: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .location-input-group {
    flex-wrap: wrap;
  }

  .btn-action-icon {
    flex: 1;
  }
}
</style>