<!-- client/src/views/camera/CameraView.vue -->
<template>
  <div class="camera-page">
    <!-- Заголовок -->
    <div class="camera-header">
      <h1 class="page-title">
        <i class="fas fa-camera me-2"></i>
        Камера
      </h1>
      <p class="page-subtitle">Сфотографируйте проблему для обращения</p>
    </div>

    <!-- Основной контейнер камеры -->
    <div class="camera-container">
      <!-- Видео поток -->
      <video
          ref="video"
          autoplay
          playsinline
          :class="{ 'camera-active': isCameraActive }"
      ></video>

      <!-- Заглушка, если камера не активна -->
      <div v-if="!isCameraActive" class="camera-placeholder">
        <i class="fas fa-camera-retro placeholder-icon"></i>
        <p class="placeholder-text">Камера неактивна</p>
        <button class="btn-start-camera" @click="startCamera">
          <i class="fas fa-power-off me-2"></i>
          Включить камеру
        </button>
      </div>

      <!-- Оверлей с сеткой (правило третей) -->
      <div v-if="isCameraActive" class="camera-grid">
        <div class="grid-line horizontal"></div>
        <div class="grid-line horizontal"></div>
        <div class="grid-line vertical"></div>
        <div class="grid-line vertical"></div>
      </div>

      <!-- Индикатор записи -->
      <div v-if="isCapturing" class="capture-indicator">
        <div class="capture-flash"></div>
      </div>
    </div>

    <!-- Панель управления -->
    <div class="camera-controls">
      <!-- Переключение камеры -->
      <button
          v-if="isCameraActive"
          class="control-btn control-btn-secondary"
          @click="switchCamera"
          title="Переключить камеру"
      >
        <i class="fas fa-sync-alt"></i>
      </button>

      <!-- Кнопка съёмки -->
      <button
          v-if="isCameraActive"
          class="control-btn control-btn-primary"
          @click="capturePhoto"
          :disabled="isCapturing"
          title="Сделать фото"
      >
        <i class="fas fa-camera"></i>
      </button>

      <!-- Галерея -->
      <button
          class="control-btn control-btn-secondary"
          @click="showGallery"
          title="Просмотреть фото"
      >
        <i class="fas fa-images"></i>
        <span v-if="capturedPhotos.length > 0" class="photo-count">
          {{ capturedPhotos.length }}
        </span>
      </button>
    </div>

    <!-- Предпросмотр сделанного фото -->
    <div v-if="previewPhoto" class="photo-preview">
      <img :src="previewPhoto" alt="Предпросмотр">
      <div class="preview-actions">
        <button class="btn-preview-action btn-retake" @click="retakePhoto">
          <i class="fas fa-redo me-2"></i>
          Переснять
        </button>
        <button class="btn-preview-action btn-save" @click="savePhoto">
          <i class="fas fa-check me-2"></i>
          Сохранить
        </button>
      </div>
    </div>

    <!-- Галерея сделанных фото -->
    <div v-if="showGalleryModal" class="gallery-modal">
      <div class="gallery-content">
        <div class="gallery-header">
          <h3>Сделанные фото ({{ capturedPhotos.length }})</h3>
          <button class="btn-close-gallery" @click="showGalleryModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="gallery-grid">
          <div
              v-for="(photo, index) in capturedPhotos"
              :key="index"
              class="gallery-item"
          >
            <img :src="photo" :alt="`Фото ${index + 1}`">
            <button class="btn-delete-photo" @click="deletePhoto(index)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
        <div v-if="capturedPhotos.length === 0" class="gallery-empty">
          <i class="fas fa-camera-retro"></i>
          <p>Пока нет фотографий</p>
        </div>
      </div>
    </div>

    <!-- Информация о камере -->
    <div class="camera-info">
      <div class="info-item">
        <i class="fas fa-info-circle"></i>
        <span>Нажмите на кнопку камеры, чтобы сделать фото</span>
      </div>
      <div class="info-item">
        <i class="fas fa-lightbulb"></i>
        <span>Используйте сетку для лучшего кадрирования</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CameraView',
  data() {
    return {
      isCameraActive: false,
      isCapturing: false,
      currentStream: null,
      facingMode: 'environment', // 'environment' = задняя камера, 'user' = фронтальная
      previewPhoto: null,
      capturedPhotos: [],
      showGalleryModal: false,
      canvas: null
    }
  },
  mounted() {
    this.canvas = document.createElement('canvas')
    this.startCamera()
  },
  beforeUnmount() {
    this.stopCamera()
  },
  methods: {
    async startCamera() {
      try {
        this.stopCamera()

        const constraints = {
          video: {
            facingMode: this.facingMode,
            width: { ideal: 1920 },
            height: { ideal: 1080 }
          }
        }

        const stream = await navigator.mediaDevices.getUserMedia(constraints)
        this.currentStream = stream
        this.$refs.video.srcObject = stream
        this.isCameraActive = true
      } catch (error) {
        console.error('Ошибка доступа к камере:', error)
        alert('Не удалось получить доступ к камере. Проверьте разрешения браузера.')
      }
    },

    stopCamera() {
      if (this.currentStream) {
        this.currentStream.getTracks().forEach(track => track.stop())
        this.currentStream = null
      }
      this.isCameraActive = false
    },

    async switchCamera() {
      this.facingMode = this.facingMode === 'environment' ? 'user' : 'environment'
      await this.startCamera()
    },

    capturePhoto() {
      if (!this.$refs.video || !this.isCameraActive) return

      this.isCapturing = true

      // Эффект вспышки
      setTimeout(() => {
        const video = this.$refs.video
        const canvas = this.canvas
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight

        const ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

        const photoData = canvas.toDataURL('image/jpeg', 0.9)
        this.previewPhoto = photoData
        this.isCapturing = false
      }, 150)
    },

    retakePhoto() {
      this.previewPhoto = null
    },

    savePhoto() {
      if (this.previewPhoto) {
        this.capturedPhotos.push(this.previewPhoto)
        this.previewPhoto = null
      }
    },

    deletePhoto(index) {
      this.capturedPhotos.splice(index, 1)
    },

    showGallery() {
      this.showGalleryModal = true
    }
  }
}
</script>

<style scoped>
.camera-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.camera-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0 0 0.5rem;
}

.page-subtitle {
  color: #70808c;
  font-size: 1rem;
  margin: 0;
}

/* Контейнер камеры */
.camera-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  margin: 0 auto 2rem;
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.15);
}

.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.camera-active {
  opacity: 1;
}

/* Заглушка */
.camera-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a2a3a 0%, #0f1a24 100%);
  color: white;
}

.placeholder-icon {
  font-size: 4rem;
  color: #00a896;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.placeholder-text {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  opacity: 0.7;
}

.btn-start-camera {
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 6px 20px rgba(0, 168, 150, 0.3);
}

.btn-start-camera:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 150, 0.4);
}

/* Сетка */
.camera-grid {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  background: rgba(255, 255, 255, 0.2);
}

.grid-line.horizontal {
  left: 0;
  right: 0;
  height: 1px;
}

.grid-line.horizontal:nth-child(1) {
  top: 33.33%;
}

.grid-line.horizontal:nth-child(2) {
  top: 66.66%;
}

.grid-line.vertical {
  top: 0;
  bottom: 0;
  width: 1px;
}

.grid-line.vertical:nth-child(3) {
  left: 33.33%;
}

.grid-line.vertical:nth-child(4) {
  left: 66.66%;
}

/* Индикатор съёмки */
.capture-indicator {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.capture-flash {
  position: absolute;
  inset: 0;
  background: white;
  opacity: 0;
  animation: flash 0.3s ease-out;
}

@keyframes flash {
  0% { opacity: 0.8; }
  100% { opacity: 0; }
}

/* Панель управления */
.camera-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.control-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  transition: all 0.2s;
  position: relative;
}

.control-btn-secondary {
  background: #f1f5f9;
  color: #172f40;
  border: 2px solid #e2e8f0;
}

.control-btn-secondary:hover {
  background: #e2e8f0;
  transform: scale(1.05);
}

.control-btn-primary {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  box-shadow: 0 8px 24px rgba(0, 168, 150, 0.3);
}

.control-btn-primary:hover:not(:disabled) {
  transform: scale(1.08);
  box-shadow: 0 10px 30px rgba(0, 168, 150, 0.4);
}

.control-btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.photo-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #c64752;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  min-width: 24px;
  text-align: center;
}

/* Предпросмотр фото */
.photo-preview {
  max-width: 800px;
  margin: 0 auto 2rem;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.15);
}

.photo-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.preview-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
}

.btn-preview-action {
  flex: 1;
  padding: 0.875rem;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-retake {
  background: #f1f5f9;
  color: #172f40;
}

.btn-retake:hover {
  background: #e2e8f0;
}

.btn-save {
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.25);
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
}

/* Модальное окно галереи */
.gallery-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.gallery-content {
  background: white;
  border-radius: 20px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
}

.gallery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.gallery-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 800;
  color: #172f40;
}

.btn-close-gallery {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  color: #172f40;
  cursor: pointer;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.btn-close-gallery:hover {
  background: #e2e8f0;
  transform: rotate(90deg);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.gallery-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  background: #f1f5f9;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-delete-photo {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(198, 71, 82, 0.9);
  color: white;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.btn-delete-photo:hover {
  background: #c64752;
  transform: scale(1.1);
}

.gallery-empty {
  text-align: center;
  padding: 3rem;
  color: #70808c;
}

.gallery-empty i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

/* Информация */
.camera-info {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  color: #172f40;
  font-size: 0.9rem;
}

.info-item i {
  color: #00a896;
  font-size: 1.25rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .camera-page {
    padding: 1.5rem 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .camera-container {
    aspect-ratio: 4/3;
  }

  .camera-controls {
    gap: 1rem;
  }

  .control-btn {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .control-btn-primary {
    width: 70px;
    height: 70px;
  }

  .preview-actions {
    flex-direction: column;
  }

  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>