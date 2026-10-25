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

        <!-- Секция 2: Локация и медиа -->
        <div class="form-section">
          <h3 class="section-title">
            <IconFa name="map-location-dot" class="me-2" /> Место реализации
          </h3>

          <div class="form-group">
            <label class="form-label">Адрес или ориентир *</label>
            <div class="input-wrapper search-wrapper" :class="{ 'is-invalid': localErrors.address }">
              <span class="input-icon"><IconFa name="magnifying-glass" /></span>
              <input
                  v-model="form.address"
                  type="text"
                  class="form-control-custom"
                  placeholder="Введите адрес, парк или ориентир..."
                  @keyup.enter.prevent="searchAddress"
              >
              <button
                  type="button"
                  class="btn-search-map"
                  @click="searchAddress"
                  :disabled="isSearching || !form.address.trim()"
              >
                <span v-if="isSearching" class="spinner-border spinner-border-sm"></span>
                <IconFa v-else name="location-crosshairs" />
              </button>
            </div>
            <div v-if="localErrors.address" class="error-message">{{ localErrors.address }}</div>
            <p class="form-hint">Найдите адрес или укажите точку прямо на карте ниже.</p>
          </div>

          <!-- Контейнер карты -->
          <div class="map-container" :class="{ 'is-invalid': localErrors.latitude }">
            <div id="initiative-map" class="map-view"></div>
            <button type="button" class="btn-geo-location" @click="getCurrentLocation" title="Моё местоположение">
              <IconFa name="crosshairs" />
            </button>
          </div>
          <div v-if="localErrors.latitude" class="error-message">Пожалуйста, укажите точку на карте</div>

          <div class="form-group mt-4">
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
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import IconFa from '@/components/ui/IconFa.vue'
import MediaUploader from '@/components/media/MediaUploader.vue'
import { useInitiativesStore } from '@/stores/initiatives.store'

export default {
  name: 'InitiativeCreateView',
  components: { IconFa, MediaUploader },
  data() {
    return {
      form: {
        title: '',
        description: '',
        address: '',
        latitude: null,
        longitude: null
      },
      files: [],
      localErrors: {},
      validationError: '',
      submitError: '',
      isSubmitting: false,
      isSearching: false,
      map: null,
      marker: null
    }
  },
  mounted() {
    this.initMap()
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove()
    }
  },
  methods: {
    initMap() {
      // Инициализация карты (центр по умолчанию, например, Москва, или можно запросить геопозицию)
      this.map = L.map('initiative-map').setView([55.7558, 37.6173], 10)

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(this.map)

      // Обработка клика по карте
      this.map.on('click', (e) => {
        this.setMarker(e.latlng.lat, e.latlng.lng)
        this.reverseGeocode(e.latlng.lat, e.latlng.lng)
      })

      // Попытка определить геопозицию пользователя при загрузке
      this.getCurrentLocation()
    },

    async searchAddress() {
      if (!this.form.address.trim()) return

      this.isSearching = true
      this.localErrors.address = ''

      try {
        // Используем бесплатный Nominatim API для геокодинга
        const response = await fetch(
            `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(this.form.address)}&limit=1`
        )
        const data = await response.json()

        if (data && data.length > 0) {
          const result = data[0]
          this.form.latitude = parseFloat(result.lat)
          this.form.longitude = parseFloat(result.lon)
          this.form.address = result.display_name // Обновляем на канонический адрес

          this.map.setView([this.form.latitude, this.form.longitude], 16)
          this.setMarker(this.form.latitude, this.form.longitude)
        } else {
          this.localErrors.address = 'Адрес не найден. Попробуйте уточнить запрос или укажите точку на карте.'
        }
      } catch (error) {
        console.error('Geocoding error:', error)
        this.localErrors.address = 'Ошибка поиска адреса. Попробуйте позже.'
      } finally {
        this.isSearching = false
      }
    },

    setMarker(lat, lng) {
      this.form.latitude = lat
      this.form.longitude = lng
      this.localErrors.latitude = ''

      if (this.marker) {
        this.marker.setLatLng([lat, lng])
      } else {
        this.marker = L.marker([lat, lng], { draggable: true }).addTo(this.map)

        // Если пользователь перетащил маркер вручную
        this.marker.on('dragend', (event) => {
          const position = event.target.getLatLng()
          this.form.latitude = position.lat
          this.form.longitude = position.lng
          this.reverseGeocode(position.lat, position.lng)
        })
      }
    },

    async reverseGeocode(lat, lng) {
      try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
        )
        const data = await response.json()
        if (data && data.display_name) {
          this.form.address = data.display_name
        }
      } catch (error) {
        console.error('Reverse geocoding error:', error)
      }
    },

    getCurrentLocation() {
      if (!navigator.geolocation) {
        this.localErrors.address = 'Геолокация не поддерживается вашим браузером'
        return
      }

      navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords
            this.form.latitude = latitude
            this.form.longitude = longitude
            this.map.setView([latitude, longitude], 15)
            this.setMarker(latitude, longitude)
            this.reverseGeocode(latitude, longitude)
          },
          () => {
            // Если пользователь запретил доступ, просто игнорируем или показываем мягкое сообщение
            console.log('Geolocation permission denied')
          }
      )
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
      if (!this.form.address.trim()) {
        this.localErrors.address = 'Укажите адрес или место'
        isValid = false
      }
      if (!this.form.latitude || !this.form.longitude) {
        this.localErrors.latitude = 'Пожалуйста, укажите точку на карте'
        isValid = false
      }

      if (!isValid) {
        this.validationError = 'Пожалуйста, проверьте правильность заполнения выделенных полей'
      }

      return isValid
    },

    async submitInitiative() {
      if (!this.validateForm()) {
        // Прокрутка к первой ошибке
        this.$nextTick(() => {
          const firstError = document.querySelector('.is-invalid')
          if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
        })
        return
      }

      this.isSubmitting = true
      this.submitError = ''
      this.validationError = ''

      try {
        const initiativesStore = useInitiativesStore()

        const payload = {
          title: this.form.title,
          description: this.form.description,
          address: this.form.address,
          latitude: this.form.latitude,
          longitude: this.form.longitude
          // files будут обработаны в сторе через FormData
        }

        await initiativesStore.createInitiative(payload, this.files)
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

.page-header-modern { margin-bottom: 1.5rem; }
.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0;
  display: flex;
  align-items: center;
}
.text-civic { color: #00a896; }
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
.form-hint {
  font-size: 0.82rem;
  color: var(--layout-muted);
  margin-top: 0.4rem;
  margin-bottom: 0;
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
  padding: 0.85rem 0.5rem 0.85rem 0;
  color: var(--layout-ink);
  font-size: 0.95rem;
  width: 100%;
  resize: vertical;
}
.form-control-custom:focus { outline: none; box-shadow: none; }
.form-control-custom::placeholder { color: #aab5bc; }

.textarea-wrapper { align-items: flex-start; }
.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: var(--layout-muted);
  margin-top: 0.35rem;
}

/* === Кнопка поиска в инпуте === */
.btn-search-map {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border: none;
  background: transparent;
  color: var(--layout-accent);
  cursor: pointer;
  transition: all 180ms ease;
  flex-shrink: 0;
}
.btn-search-map:hover:not(:disabled) {
  background: rgba(0, 168, 150, 0.08);
}
.btn-search-map:disabled {
  color: var(--layout-muted);
  cursor: not-allowed;
  opacity: 0.5;
}

/* === Карта === */
.map-container {
  position: relative;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  overflow: hidden;
  background: #fcfcfd;
  transition: all 180ms ease;
  height: 350px;
}
.map-container:focus-within, .map-container:hover {
  border-color: var(--layout-accent);
  box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
}
.map-container.is-invalid {
  border-color: #c64752;
  background: #fff0f1;
}

.map-view {
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* Кнопка геолокации на карте */
.btn-geo-location {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 1000;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #ffffff;
  color: var(--layout-ink);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 180ms ease;
}
.btn-geo-location:hover {
  background: var(--layout-accent);
  color: #ffffff;
  transform: scale(1.05);
}

/* === Ошибки и действия === */
.error-message {
  margin-top: 0.4rem;
  color: #c64752;
  font-size: 0.82rem;
  font-weight: 600;
}

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
  .map-container { height: 250px; }
}
</style>