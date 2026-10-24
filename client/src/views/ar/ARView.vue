<!-- client/src/views/ar/ARView.vue -->
<template>
  <div class="ar-page">
    <!-- AR Header -->
    <div class="ar-header">
      <button class="ar-back-btn" @click="goBack">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h1 class="ar-title">AR-режим</h1>
      <button class="ar-info-btn" @click="showInfo = !showInfo">
        <i class="fas fa-info-circle"></i>
      </button>
    </div>

    <!-- AR Container -->
    <div ref="arContainer" class="ar-container">
      <!-- Видео с камеры (фон) -->
      <video
          ref="video"
          autoplay
          playsinline
          class="ar-video"
      ></video>

      <!-- Three.js Canvas (поверх видео) -->
      <canvas ref="canvas" class="ar-canvas"></canvas>

      <!-- Загрузка -->
      <div v-if="isLoading" class="ar-loading">
        <div class="loading-spinner"></div>
        <p>Загрузка AR-режима...</p>
      </div>

      <!-- Ошибка -->
      <div v-if="error" class="ar-error">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ error }}</p>
        <button @click="initAR" class="btn-retry">
          <i class="fas fa-redo me-2"></i>
          Повторить
        </button>
      </div>
    </div>

    <!-- Информационная панель -->
    <div v-if="showInfo" class="info-panel">
      <div class="info-content">
        <h3>Как использовать AR-режим</h3>
        <ul>
          <li>
            <i class="fas fa-map-marker-alt"></i>
            <span>Красные маркеры — критические проблемы</span>
          </li>
          <li>
            <i class="fas fa-map-marker-alt" style="color: #fd7e14;"></i>
            <span>Оранжевые маркеры — проблемы в работе</span>
          </li>
          <li>
            <i class="fas fa-map-marker-alt" style="color: #00a896;"></i>
            <span>Зелёные маркеры — решённые проблемы</span>
          </li>
          <li>
            <i class="fas fa-hand-pointer"></i>
            <span>Нажмите на маркер для подробной информации</span>
          </li>
        </ul>
        <button @click="showInfo = false" class="btn-close-info">
          Понятно
        </button>
      </div>
    </div>

    <!-- Панель выбранного маркера -->
    <div v-if="selectedMarker" class="marker-panel">
      <div class="marker-content">
        <div class="marker-header">
          <div
              class="marker-status"
              :style="{ background: getStatusColor(selectedMarker.status) }"
          ></div>
          <h3>{{ selectedMarker.title }}</h3>
          <button @click="closeMarker" class="btn-close-marker">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <p class="marker-description">{{ selectedMarker.description }}</p>
        <div class="marker-meta">
          <div class="meta-item">
            <i class="fas fa-calendar"></i>
            <span>{{ formatDate(selectedMarker.date) }}</span>
          </div>
          <div class="meta-item">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ selectedMarker.address }}</span>
          </div>
        </div>
        <div class="marker-actions">
          <button class="btn-marker-action btn-details">
            <i class="fas fa-info-circle me-2"></i>
            Подробнее
          </button>
          <button class="btn-marker-action btn-navigate">
            <i class="fas fa-route me-2"></i>
            Проложить маршрут
          </button>
        </div>
      </div>
    </div>

    <!-- Нижняя панель управления (компактные иконки) -->
    <div class="ar-controls">
      <button
          class="control-btn"
          :class="{ active: filterStatus === 'all' }"
          @click="setFilter('all')"
          title="Все проблемы"
      >
        <i class="fas fa-layer-group"></i>
        <span class="control-badge">{{ (markerMeshes || []).length }}</span>
      </button>

      <button
          class="control-btn control-btn--critical"
          :class="{ active: filterStatus === 'critical' }"
          @click="setFilter('critical')"
          title="Критические"
      >
        <i class="fas fa-exclamation-circle"></i>
        <span class="control-badge">{{ criticalCount }}</span>
      </button>

      <button
          class="control-btn control-btn--progress"
          :class="{ active: filterStatus === 'in_progress' }"
          @click="setFilter('in_progress')"
          title="В работе"
      >
        <i class="fas fa-spinner"></i>
        <span class="control-badge">{{ progressCount }}</span>
      </button>

      <button
          class="control-btn control-btn--resolved"
          :class="{ active: filterStatus === 'resolved' }"
          @click="setFilter('resolved')"
          title="Решённые"
      >
        <i class="fas fa-check-circle"></i>
        <span class="control-badge">{{ resolvedCount }}</span>
      </button>
    </div>

    <!-- Счётчик маркеров -->
    <div class="markers-counter">
      <i class="fas fa-map-marker-alt"></i>
      <span>{{ (markerMeshes || []).length }} маркеров</span>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'

export default {
  name: 'ARView',

  // Все реактивные данные должны быть внутри data()
  data() {
    return {
      selectedMarker: null,
      filterStatus: 'all',
      isLoading: true,
      error: null,
      showInfo: false,
      markerMeshes: [], // <-- Перенесено сюда для корректной инициализации
      stream: null,
      animationId: null,
      raycaster: null,
      mouse: null
    }
  },

  // НЕРЕАКТИВНЫЕ свойства Three.js (Vue не будет их проксировать)
  scene: null,
  camera: null,
  renderer: null,

  computed: {
    visibleMarkers() {
      // Безопасная проверка: если массив еще не создан, возвращаем пустой
      const meshes = this.markerMeshes || []

      if (this.filterStatus === 'all') {
        return meshes
      }

      return meshes.filter(marker =>
          marker.userData && marker.userData.status === this.filterStatus
      )
    }
  },

  mounted() {
    this.initAR()
    window.addEventListener('resize', this.onResize)
  },

  beforeUnmount() {
    this.cleanup()
    window.removeEventListener('resize', this.onResize)
  },

  methods: {
    async initAR() {
      try {
        this.isLoading = true
        this.error = null

        await this.initCamera()
        this.initThreeJS()
        this.createTestMarkers()

        this.isLoading = false
        this.animate()
      } catch (error) {
        console.error('AR initialization error:', error)
        this.error = 'Не удалось инициализировать AR-режим. Проверьте разрешения камеры.'
        this.isLoading = false
      }
    },

    async initCamera() {
      const constraints = {
        video: {
          facingMode: 'environment',
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      }

      this.stream = await navigator.mediaDevices.getUserMedia(constraints)
      if (this.$refs.video) {
        this.$refs.video.srcObject = this.stream
      }
    },

    initThreeJS() {
      const container = this.$refs.arContainer
      if (!container) return

      const width = container.clientWidth
      const height = container.clientHeight

      this.scene = new THREE.Scene()

      this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
      this.camera.position.z = 5

      this.renderer = new THREE.WebGLRenderer({
        canvas: this.$refs.canvas,
        alpha: true,
        antialias: true
      })
      this.renderer.setSize(width, height)
      this.renderer.setPixelRatio(window.devicePixelRatio)

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
      this.scene.add(ambientLight)

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
      directionalLight.position.set(10, 10, 5)
      this.scene.add(directionalLight)

      this.raycaster = new THREE.Raycaster()
      this.mouse = new THREE.Vector2()

      if (this.$refs.canvas) {
        this.$refs.canvas.addEventListener('click', this.onCanvasClick)
      }
    },

    createTestMarkers() {
      const testData = [
        {
          id: 1,
          title: 'Яма на дороге',
          description: 'Большая яма на проезжей части, опасна для транспорта',
          status: 'critical',
          address: 'ул. Ленина, д. 10',
          date: '2024-10-15',
          position: { x: -2, y: 1, z: -3 }
        },
        {
          id: 2,
          title: 'Сломанная лавочка',
          description: 'Лавочка в парке сломана, требуется ремонт',
          status: 'in_progress',
          address: 'Парк культуры',
          date: '2024-10-18',
          position: { x: 1.5, y: 0.5, z: -4 }
        },
        {
          id: 3,
          title: 'Не работает фонарь',
          description: 'Уличное освещение не работает уже неделю',
          status: 'resolved',
          address: 'ул. Пушкина, д. 5',
          date: '2024-10-10',
          position: { x: 0, y: 2, z: -5 }
        },
        {
          id: 4,
          title: 'Мусор на улице',
          description: 'Несанкционированная свалка мусора',
          status: 'critical',
          address: 'ул. Гагарина, д. 15',
          date: '2024-10-20',
          position: { x: -1, y: -0.5, z: -3.5 }
        },
        {
          id: 5,
          title: 'Прорыв трубы',
          description: 'Течёт вода из подземной трубы',
          status: 'in_progress',
          address: 'ул. Советская, д. 8',
          date: '2024-10-19',
          position: { x: 2.5, y: 1.5, z: -4.5 }
        }
      ]

      testData.forEach(data => {
        this.createMarker(data)
      })
    },

    createMarker(data) {
      const group = new THREE.Group()
      const color = this.getStatusColor3D(data.status)

      // Конус
      const geometry = new THREE.ConeGeometry(0.2, 0.6, 32)
      const material = new THREE.MeshPhongMaterial({
        color: color,
        emissive: color,
        emissiveIntensity: 0.3,
        shininess: 100
      })
      const cone = new THREE.Mesh(geometry, material)
      cone.rotation.x = Math.PI
      group.add(cone)

      // Сфера на вершине
      const sphereGeometry = new THREE.SphereGeometry(0.15, 32, 32)
      const sphereMaterial = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        emissive: color,
        emissiveIntensity: 0.5
      })
      const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial)
      sphere.position.y = 0.4
      group.add(sphere)

      // Кольцо вокруг
      const ringGeometry = new THREE.RingGeometry(0.3, 0.35, 32)
      const ringMaterial = new THREE.MeshBasicMaterial({
        color: color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.5
      })
      const ring = new THREE.Mesh(ringGeometry, ringMaterial)
      ring.rotation.x = -Math.PI / 2
      ring.position.y = -0.3
      group.add(ring)

      group.position.set(data.position.x, data.position.y, data.position.z)
      group.userData = { ...data, isMarker: true }

      this.scene.add(group)
      this.markerMeshes.push(group)
    },

    getStatusColor3D(status) {
      const colors = {
        critical: 0xc64752,
        in_progress: 0xfd7e14,
        resolved: 0x00a896
      }
      return colors[status] || 0x808080
    },

    getStatusColor(status) {
      const colors = {
        critical: '#c64752',
        in_progress: '#fd7e14',
        resolved: '#00a896'
      }
      return colors[status] || '#808080'
    },

    animate() {
      this.animationId = requestAnimationFrame(this.animate)

      // Вращаем только видимые маркеры
      this.visibleMarkers.forEach(marker => {
        marker.rotation.y += 0.01
        marker.position.y += Math.sin(Date.now() * 0.001) * 0.001
      })

      if (this.renderer && this.scene && this.camera) {
        this.renderer.render(this.scene, this.camera)
      }
    },

    onCanvasClick(event) {
      if (!this.$refs.canvas || !this.camera) return

      const rect = this.$refs.canvas.getBoundingClientRect()
      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
      this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

      this.raycaster.setFromCamera(this.mouse, this.camera)

      // Собираем все дочерние объекты видимых маркеров для проверки пересечений
      const objectsToCheck = []
      this.visibleMarkers.forEach(marker => {
        marker.traverse(child => {
          objectsToCheck.push(child)
        })
      })

      const intersects = this.raycaster.intersectObjects(objectsToCheck, true)

      if (intersects.length > 0) {
        // Находим родительский Group, который содержит userData
        let target = intersects[0].object
        while (target.parent && !target.userData.isMarker) {
          target = target.parent
        }

        if (target.userData.isMarker) {
          this.selectedMarker = target.userData
        } else {
          this.selectedMarker = null
        }
      } else {
        this.selectedMarker = null
      }
    },

    setFilter(status) {
      this.filterStatus = status

      // Обновляем видимость маркеров
      this.markerMeshes.forEach(marker => {
        if (status === 'all' || marker.userData.status === status) {
          marker.visible = true
        } else {
          marker.visible = false
        }
      })
    },

    closeMarker() {
      this.selectedMarker = null
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    onResize() {
      if (!this.camera || !this.renderer || !this.$refs.arContainer) return

      const container = this.$refs.arContainer
      const width = container.clientWidth
      const height = container.clientHeight

      this.camera.aspect = width / height
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(width, height)
    },

    goBack() {
      this.$router.push('/map')
    },

    cleanup() {
      if (this.animationId) {
        cancelAnimationFrame(this.animationId)
      }

      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop())
      }

      if (this.renderer) {
        this.renderer.dispose()
      }

      if (this.$refs.canvas) {
        this.$refs.canvas.removeEventListener('click', this.onCanvasClick)
      }

      // Очистка сцены
      if (this.scene) {
        this.scene.traverse(object => {
          if (object.geometry) object.geometry.dispose()
          if (object.material) {
            if (Array.isArray(object.material)) {
              object.material.forEach(m => m.dispose())
            } else {
              object.material.dispose()
            }
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.ar-page {
  position: fixed;
  inset: 0;
  background: #000;
  overflow: hidden;
}

.ar-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), transparent);
}

.ar-back-btn,
.ar-info-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.ar-back-btn:hover,
.ar-info-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.ar-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.ar-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.ar-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ar-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.ar-loading,
.ar-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  z-index: 200;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #00a896;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.ar-error i {
  font-size: 3rem;
  color: #c64752;
  margin-bottom: 1rem;
}

.ar-error p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  text-align: center;
  padding: 0 2rem;
}

.btn-retry {
  padding: 0.75rem 1.5rem;
  background: #00a896;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-retry:hover {
  background: #008f80;
  transform: translateY(-2px);
}

/* Информационная панель */
.info-panel {
  position: absolute;
  top: 80px;
  left: 1rem;
  right: 1rem;
  z-index: 150;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.info-content h3 {
  margin: 0 0 1rem;
  color: #172f40;
  font-size: 1.25rem;
  font-weight: 700;
}

.info-content ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
}

.info-content li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  color: #172f40;
  font-size: 0.95rem;
}

.info-content li i {
  width: 24px;
  text-align: center;
  font-size: 1.1rem;
}

.btn-close-info {
  width: 100%;
  padding: 0.875rem;
  background: #00a896;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-close-info:hover {
  background: #008f80;
}

/* Панель маркера */
.marker-panel {
  position: absolute;
  bottom: 120px;
  left: 1rem;
  right: 1rem;
  z-index: 150;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.marker-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.marker-status {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.marker-header h3 {
  flex: 1;
  margin: 0;
  color: #172f40;
  font-size: 1.1rem;
  font-weight: 700;
}

.btn-close-marker {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  color: #172f40;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-close-marker:hover {
  background: #e2e8f0;
  transform: rotate(90deg);
}

.marker-description {
  color: #70808c;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 1rem;
}

.marker-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #172f40;
  font-size: 0.9rem;
}

.meta-item i {
  color: #00a896;
  width: 20px;
}

.marker-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-marker-action {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-details {
  background: #f1f5f9;
  color: #172f40;
}

.btn-details:hover {
  background: #e2e8f0;
}

.btn-navigate {
  background: #00a896;
  color: white;
}

.btn-navigate:hover {
  background: #008f80;
  transform: translateY(-2px);
}

/* Нижняя панель управления */
.ar-controls {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 12px;
}

.control-btn i {
  font-size: 1.25rem;
}

.control-btn.active {
  background: rgba(0, 168, 150, 0.8);
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Счётчик маркеров */
.markers-counter {
  position: absolute;
  top: 80px;
  right: 1rem;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
}

.markers-counter i {
  color: #00a896;
}

@media (max-width: 768px) {
  .ar-controls {
    bottom: 10px;
    gap: 0.25rem;
  }

  .control-btn {
    padding: 0.4rem 0.5rem;
    font-size: 0.7rem;
  }

  .control-btn i {
    font-size: 1rem;
  }

  .marker-panel {
    bottom: 100px;
  }
}
</style>