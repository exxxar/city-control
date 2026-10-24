<!-- client/src/views/ar/ProblemArView.vue -->
<template>
  <div class="ar-view position-fixed top-0 start-0 w-100 h-100 bg-black">
    <!-- Camera stream -->
    <video
      ref="videoElement"
      class="position-absolute top-0 start-0 w-100 h-100"
      style="object-fit: cover;"
      autoplay
      playsinline
    ></video>

    <!-- Three.js canvas -->
    <div ref="arContainer" class="position-absolute top-0 start-0 w-100 h-100"></div>

    <!-- UI Overlay -->
    <div class="position-absolute top-0 start-0 w-100 h-100 d-flex flex-column">
      <!-- Header -->
      <div class="ar-header bg-dark bg-opacity-75 text-white p-3">
        <div class="d-flex justify-content-between align-items-center">
          <button class="btn btn-link text-white p-0" @click="exitAr">
            <IconFa name="x-lg" size="1.5rem" />
          </button>
          <h6 class="mb-0">AR-режим</h6>
          <div class="ar-stats">
            <IconFa name="geo-alt" class="me-1" />
            <span>{{ nearbyProblems.length }} проблем рядом</span>
          </div>
        </div>
      </div>

      <!-- Spacer -->
      <div class="flex-grow-1"></div>

      <!-- Problem card (when marker clicked) -->
      <Transition name="slide-up">
        <div v-if="selectedProblem" class="ar-problem-card bg-white rounded-top-3 p-3 shadow-lg">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <div class="flex-grow-1">
              <ProblemStatusBadge :status="selectedProblem.status" size="sm" />
              <h6 class="mt-2 mb-1 fw-bold">{{ selectedProblem.title }}</h6>
              <small class="text-muted">{{ selectedProblem.description }}</small>
            </div>
            <button class="btn btn-sm btn-link text-secondary" @click="selectedProblem = null">
              <IconFa name="x-lg" />
            </button>
          </div>
          <div class="d-flex gap-2">
            <router-link
              :to="`/problems/${selectedProblem.id}/details`"
              class="btn btn-civic flex-grow-1"
            >
              Открыть карточку
            </router-link>
          </div>
        </div>
      </Transition>

      <!-- Instructions -->
      <div v-if="!selectedProblem" class="ar-instructions bg-dark bg-opacity-75 text-white text-center p-3">
        <IconFa name="camera" size="2rem" class="mb-2" />
        <p class="mb-0 small">Наведите камеру на проблему</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="position-absolute top-50 start-50 translate-middle text-white text-center">
      <div class="spinner-border mb-3"></div>
      <p>Инициализация AR...</p>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import ProblemStatusBadge from '@/components/problems/ProblemStatusBadge.vue'
import { arService } from '@/services/ar.service'
import { cameraService } from '@/services/camera.service'
import * as problemsApi from '@/api/problems.api'

export default {
  name: 'ProblemArView',
  components: { IconFa, ProblemStatusBadge },
  props: {
    problemId: { type: [String, Number], required: true }
  },
  data() {
    return {
      isLoading: true,
      nearbyProblems: [],
      selectedProblem: null
    }
  },
  async mounted() {
    await this.initAr()
  },
  beforeUnmount() {
    this.cleanup()
  },
  methods: {
    async initAr() {
      this.isLoading = true

      try {
        // Запускаем камеру
        await cameraService.startStream(this.$refs.videoElement)

        // Инициализируем Three.js сцену
        arService.init(this.$refs.arContainer)

        // Загружаем ближайшие проблемы
        await this.loadNearbyProblems()

        // Добавляем маркеры на сцену
        this.renderArMarkers()

        // Запускаем анимацию
        arService.start()

        // Обработчик клика по маркерам
        this.$refs.arContainer.addEventListener('click', this.handleArClick)

      } catch (error) {
        console.error('AR initialization error:', error)
        alert('Не удалось запустить AR-режим')
        this.$router.back()
      } finally {
        this.isLoading = false
      }
    },

    async loadNearbyProblems() {
      try {
        // Получаем текущую проблему
        const mainProblem = await problemsApi.getProblem(this.problemId)

        // Загружаем ближайшие проблемы (в реальности - spatial query)
        this.nearbyProblems = [mainProblem]

        // TODO: Загрузить другие проблемы рядом через API
      } catch (error) {
        console.error('Failed to load nearby problems:', error)
      }
    },

    renderArMarkers() {
      this.nearbyProblems.forEach((problem, index) => {
        // Позиция маркера (в реальности - из GPS/гео-метки)
        const position = {
          x: (index - 1) * 2, // Расставляем маркеры в ряд
          y: 0,
          z: -5 // 5 метров перед камерой
        }

        arService.addProblemMarker(problem, position)
      })
    },

    handleArClick(event) {
      const problem = arService.onClick(event, this.$refs.arContainer)
      if (problem) {
        this.selectedProblem = problem
      }
    },

    exitAr() {
      this.$router.back()
    },

    cleanup() {
      cameraService.stopStream()
      arService.destroy()
    }
  }
}
</script>

<style scoped>
.ar-header {
  z-index: 10;
}

.ar-stats {
  font-size: 0.875rem;
}

.ar-problem-card {
  z-index: 10;
  max-width: 500px;
  margin: 0 auto;
}

.ar-instructions {
  z-index: 10;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>