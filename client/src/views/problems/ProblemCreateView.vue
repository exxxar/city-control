<!-- client/src/views/problems/ProblemCreateView.vue -->
<template>
  <div class="form-container pt-5">

    <!-- === ЗАГОЛОВОК СТРАНИЦЫ === -->
    <div class="page-header-modern">
      <div>
        <h2 class="page-title">
          <IconFa name="circle-exclamation" class="me-2" />
          Сообщить о проблеме
        </h2>
        <p class="page-subtitle">
          Опишите проблему, прикрепите фото и укажите место. Мы передадим обращение ответственным службам.
        </p>
      </div>
    </div>

    <!-- === НОВЫЙ БЛОК: Список черновиков === -->
    <Transition name="slide-down">
      <div v-if="drafts.length > 0" class="drafts-panel">
        <div class="drafts-header">
          <IconFa name="clock-rotate-left" class="me-2" />
          <span>Сохраненные черновики</span>
        </div>

        <div class="drafts-list">
          <div v-for="draft in drafts" :key="draft.id" class="draft-item">
            <div class="draft-info">
              <span class="draft-title">{{ draft.title || 'Без названия' }}</span>
              <span class="draft-meta">
                {{ formatDate(draft.createdAt) }}
                <span v-if="!draft.latitude" class="text-warning">(без координат)</span>
              </span>
            </div>
            <div class="draft-actions">
              <button type="button" class="btn-restore" @click="restoreDraft(draft)" title="Восстановить данные в форму">
                <IconFa name="arrow-rotate-left" class="me-1" /> Восстановить
              </button>
              <button type="button" class="btn-delete" @click="deleteDraft(draft.id)" title="Удалить черновик">
                <IconFa name="trash-can" />
              </button>
            </div>
          </div>
        </div>
        <p class="drafts-hint">
          <IconFa name="info-circle" class="me-1" />
          При восстановлении данные заполнят форму. Фотографии потребуется прикрепить заново.
        </p>
      </div>
    </Transition>

    <form @submit.prevent="submitProblem" class="modern-form">

      <!-- Секция 1: Основная информация -->
      <div class="form-section">
        <h3 class="section-title">
          <IconFa name="circle-info" class="me-2" /> Основная информация
        </h3>

        <!-- Категории в виде карточек -->
        <div class="form-group">
          <span class="form-label">Категория проблемы *</span>
          <div
              class="category-grid"
              :class="{ 'is-invalid': errors.category_id }"
              role="radiogroup"
              aria-label="Категория проблемы"
          >
            <button
                v-for="cat in categories"
                :key="cat.id"
                type="button"
                class="category-card"
                :class="{ 'is-selected': Number(form.category_id) === Number(cat.id) }"
                role="radio"
                :aria-checked="Number(form.category_id) === Number(cat.id)"
                @click="selectCategory(cat.id)"
            >
                <span class="category-card-icon" aria-hidden="true">
                  <IconFa :name="categoryIcon(cat)" />
                </span>
              <span class="category-card-name">{{ cat.name }}</span>
              <span v-if="cat.description" class="category-card-description">
                  {{ cat.description }}
                </span>
              <span v-if="Number(form.category_id) === Number(cat.id)" class="category-card-check" aria-hidden="true">
                  <IconFa name="check-circle" />
                </span>
            </button>
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

    <!-- Модальное окно выбора на карте -->
    <MapPickerModal
        v-model="showMapModal"
        :initial-lat="form.latitude"
        :initial-lng="form.longitude"
        @select="onLocationSelected"
    />
  </div>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import MediaUploader from '@/components/media/MediaUploader.vue'
import { useProblemsStore } from '@/stores/problems.store'
import { useOfflineQueue } from '@/composables/useOfflineQueue'
import * as categoriesApi from '@/api/categories.api'
import MapPickerModal from '@/components/map/MapPickerModal.vue'

export default {
  name: 'ProblemCreateView',
  components: {
    AppPageContainer,
    IconFa,
    MediaUploader,
    MapPickerModal
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
      locationText: '',
      drafts: [],
      showMapModal: false
    }
  },
  async mounted() {
    await this.loadCategories()
    this.loadDrafts()
    this.detectLocation()
  },
  methods: {
    loadDrafts() {
      const { getDrafts } = useOfflineQueue()
      this.drafts = getDrafts()
    },

    restoreDraft(draft) {
      this.form = {
        category_id: draft.category_id || '',
        title: draft.title || '',
        description: draft.description || '',
        latitude: draft.latitude || null,
        longitude: draft.longitude || null,
        territory_id: draft.territory_id || null,
        geo_tag_id: draft.geo_tag_id || null
      }

      if (draft.latitude && draft.longitude) {
        this.locationText = `${draft.latitude.toFixed(5)}, ${draft.longitude.toFixed(5)}`
      } else {
        this.locationText = 'Не указано'
      }

      this.files = []
      this.errors = {}

      this.deleteDraft(draft.id)

      this.$nextTick(() => {
        document.querySelector('.modern-form')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      })
    },

    deleteDraft(id) {
      const { removeDraft } = useOfflineQueue()
      removeDraft(id)
      this.loadDrafts()
    },

    formatDate(isoString) {
      if (!isoString) return ''
      const date = new Date(isoString)
      return date.toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    onLocationSelected(data) {
      this.form.latitude = data.lat
      this.form.longitude = data.lng
      this.locationText = data.address || `${data.lat.toFixed(5)}, ${data.lng.toFixed(5)}`
    },

    selectCategory(categoryId) {
      this.form.category_id = categoryId
      if (this.errors.category_id) {
        delete this.errors.category_id
      }
    },

    categoryIcon(category) {
      const icons = {
        1: 'city',
        2: 'house-chimney',
        3: 'car-side',
        4: 'shield-halved',
        5: 'leaf',
        6: 'people-group',
        7: 'notes-medical',
        8: 'graduation-cap',
        9: 'file-lines',
        10: 'briefcase',
        11: 'landmark',
        12: 'masks-theater',
        27: 'road',
        28: 'tree',
        29: 'lightbulb'
      }
      return icons[Number(category.id)] || 'tag'
    },

    async loadCategories() {
      try {
        const response = await categoriesApi.getCategories()
        this.categories = response.data || response || []
      } catch (error) {
        console.error('Failed to load categories:', error)
        this.categories = [
          { id: 1, name: 'Благоустройство и городская среда', description: 'Проблемы, связанные с состоянием городской инфраструктуры.' },
          { id: 2, name: 'ЖКХ и коммунальные услуги', description: 'Коммунальные проблемы: вода, отопление, электричество.' },
          { id: 3, name: 'Транспорт и безопасность', description: 'Проблемы транспорта, парковок и дорожной безопасности.' },
          { id: 4, name: 'Правопорядок и общественная безопасность', description: 'Нарушения общественного порядка и вопросы безопасности.' },
          { id: 5, name: 'Экология и окружающая среда', description: 'Экологические проблемы и вопросы обращения с отходами.' },
          { id: 6, name: 'Социальная сфера', description: 'Социальная поддержка, помощь семьям, пенсионерам и малоимущим.' },
          { id: 7, name: 'Здравоохранение', description: 'Проблемы медицинского обслуживания и доступности услуг.' },
          { id: 8, name: 'Образование', description: 'Проблемы школ, детских садов и образовательных учреждений.' },
          { id: 9, name: 'Административные услуги', description: 'Проблемы взаимодействия с МФЦ и госуслугами.' },
          { id: 10, name: 'Труд и занятость', description: 'Проблемы трудовых отношений и занятости.' },
          { id: 11, name: 'Взаимодействие с органами власти', description: 'Проблемы коммуникации с чиновниками и госструктурами.' },
          { id: 12, name: 'Культура, спорт и мероприятия', description: 'Проблемы организации мероприятий и доступности культурных объектов.' },
          { id: 27, name: 'Дороги и тротуары', description: 'Состояние дорог, тротуаров и пешеходных зон.' },
          { id: 28, name: 'Благоустройство', description: 'Озеленение и благоустройство общественных пространств.' },
          { id: 29, name: 'Освещение', description: 'Неисправное или недостаточное уличное освещение.' }
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
      this.showMapModal = true
    },

    async submitProblem() {
      console.log('[DEBUG] submitProblem вызван')

      this.errors = {}

      console.log('[DEBUG] form:', JSON.stringify(this.form))

      if (!this.form.category_id) {
        this.errors.category_id = 'Выберите категорию'
        return
      }

      if (!this.form.title.trim()) {
        this.errors.title = 'Введите заголовок'
        return
      }

      if (!this.form.description.trim() ||
          this.form.description.trim().length < 10) {
        this.errors.description =
            'Описание должно содержать минимум 10 символов'
        return
      }

      this.isSubmitting = true

      try {
        const problemsStore = useProblemsStore()
        const response = await problemsStore.createProblem(this.form)

        console.log('[DEBUG] Ответ создания:', response)

        const problemId = response?.id ?? response?.problem?.id ?? response?.data?.id

        console.log("ID", problemId)

        if (problemId == null) {
          console.error('[DEBUG] Сервер не вернул ID обращения:', response)
          this.errors.form = 'Обращение создано, но ID не получен от сервера.'
          return
        }

        await this.$router.push({
          name: 'ProblemDetails',
          params: { id: problemId }
        })
      } catch (error) {
        console.error('[DEBUG] Ошибка:', error)
        console.error('[DEBUG] Ответ API:', error.response?.data)

      } finally {
        this.isSubmitting = false
      }
    },

    saveToOfflineQueue() {
      try {
        const { addProblemToQueue } = useOfflineQueue()
        addProblemToQueue({ ...this.form, files: this.files })

        this.loadDrafts()

        alert('Обращение сохранено в черновики')
      } catch (error) {
        console.error('Offline queue error:', error)
        alert('Ошибка сохранения в черновики')
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

/* === Заголовок страницы === */
.page-header-modern {
  margin-bottom: 1.5rem;
  padding: 0 0.25rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--layout-ink);
  letter-spacing: -0.03em;
  margin: 0;
  display: flex;
  align-items: center;
}

.page-subtitle {
  color: var(--layout-muted);
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
  line-height: 1.5;
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

/* === Выбор категории карточками === */
.category-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
}

.category-grid.is-invalid {
  padding: 0.35rem;
  border: 1px solid #c64752;
  border-radius: 16px;
}

.category-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.55rem;
  min-width: 0;
  min-height: 150px;
  padding: 1rem;
  border: 1px solid var(--layout-line);
  border-radius: 16px;
  background: #ffffff;
  color: var(--layout-ink);
  text-align: left;
  cursor: pointer;
  transition: border-color 180ms ease, background 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}

.category-card:hover {
  border-color: var(--layout-accent);
  background: #f8fffe;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(23, 47, 64, 0.07);
}

.category-card:focus-visible {
  outline: 3px solid rgba(0, 168, 150, 0.25);
  outline-offset: 2px;
}

.category-card.is-selected {
  border-color: var(--layout-accent);
  background: rgba(0, 168, 150, 0.07);
  box-shadow: 0 0 0 2px rgba(0, 168, 150, 0.12);
}

.category-card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  border-radius: 12px;
  background: #eef8f7;
  color: var(--layout-accent);
  font-size: 1.25rem;
}

.category-card.is-selected .category-card-icon {
  background: var(--layout-accent);
  color: #ffffff;
}

.category-card-name {
  padding-right: 0.25rem;
  font-size: 0.9rem;
  font-weight: 750;
  line-height: 1.35;
}

.category-card-description {
  color: var(--layout-muted);
  font-size: 0.78rem;
  line-height: 1.45;
}

.category-card-check {
  position: absolute;
  top: 0.7rem;
  right: 0.7rem;
  color: var(--layout-accent);
  font-size: 1.05rem;
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

/* === Панель черновиков === */
.drafts-panel {
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 16px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(23, 47, 64, 0.03);
}

.drafts-header {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--layout-ink);
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--layout-line);
}

.drafts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.draft-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem;
  background: #fcfcfd;
  border: 1px solid var(--layout-line);
  border-radius: 12px;
  transition: all 180ms ease;
}

.draft-item:hover {
  border-color: var(--layout-accent);
  background: #f8fffe;
}

.draft-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  min-width: 0;
}

.draft-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--layout-ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.draft-meta {
  font-size: 0.78rem;
  color: var(--layout-muted);
}

.text-warning {
  color: #d97706;
}

.draft-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
  margin-left: 1rem;
}

.btn-restore {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.85rem;
  border: none;
  border-radius: 8px;
  background: var(--layout-accent);
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 180ms ease;
}

.btn-restore:hover {
  background: #008f80;
  transform: translateY(-1px);
}

.btn-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid var(--layout-line);
  border-radius: 8px;
  background: transparent;
  color: var(--layout-muted);
  cursor: pointer;
  transition: all 180ms ease;
}

.btn-delete:hover {
  border-color: #c64752;
  color: #c64752;
  background: #fff0f1;
}

.drafts-hint {
  margin-top: 1rem;
  margin-bottom: 0;
  font-size: 0.78rem;
  color: var(--layout-muted);
  display: flex;
  align-items: flex-start;
}

/* === Анимации === */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .page-header-modern {
    margin-bottom: 1.25rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.88rem;
  }

  .category-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.65rem;
  }

  .category-card {
    min-height: 135px;
    padding: 0.8rem;
  }

  .category-card-name {
    font-size: 0.84rem;
  }

  .category-card-description {
    font-size: 0.74rem;
  }

  .modern-form {
    padding: 1.5rem 1.25rem;
    border-radius: 16px;
  }

  .location-input-group {
    flex-wrap: wrap;
  }

  .btn-action-icon {
    flex: 1;
  }

  .draft-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .draft-actions {
    width: 100%;
    margin-left: 0;
  }

  .btn-restore {
    flex: 1;
    justify-content: center;
  }
}
</style>