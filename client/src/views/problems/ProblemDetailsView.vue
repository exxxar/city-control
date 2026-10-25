<!-- client/src/views/problems/ProblemDetailsView.vue -->
<template>
  <AppPageContainer>
    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка информации об обращении...</p>
    </div>

    <!-- Состояние: не найдено -->
    <div v-else-if="!problem" class="empty-state">
      <IconFa name="exclamation-triangle" class="empty-icon" />
      <h3>Обращение не найдено</h3>
      <p>Возможно, оно было удалено или у вас нет прав для его просмотра.</p>
      <router-link to="/problems" class="btn btn-primary">Вернуться к списку</router-link>
    </div>

    <!-- Основной контент -->
    <div v-else class="problem-details">
      <!-- Шапка: Статус и приоритет -->
      <div class="details-header">
        <div class="badges-group">
          <ProblemStatusBadge :status="problem.status" />
          <span v-if="problem.priority_id === 1" class="badge badge-danger">
            <IconFa name="fire" class="me-1" /> Критическая
          </span>
          <span v-else-if="problem.priority_id === 2" class="badge badge-warning">
            <IconFa name="exclamation-circle" class="me-1" /> Высокая
          </span>
        </div>
        <div class="problem-id">ID: #{{ problem.id }}</div>
      </div>

      <!-- Заголовок и описание -->
      <h1 class="problem-title">{{ problem.title }}</h1>
      <div class="problem-description">
        <p>{{ problem.description || 'Описание не указано' }}</p>
      </div>

      <!-- Мета-информация (Сетка) -->
      <div class="meta-card">
        <div class="meta-item">
          <IconFa name="calendar-alt" class="meta-icon" />
          <div class="meta-content">
            <span class="meta-label">Дата создания</span>
            <span class="meta-value">{{ formatDate(problem.created_at) }}</span>
          </div>
        </div>
        <div class="meta-item">
          <IconFa name="user" class="meta-icon" />
          <div class="meta-content">
            <span class="meta-label">Автор</span>
            <span class="meta-value">{{ problem.created_by?.full_name || 'Аноним' }}</span>
          </div>
        </div>
        <div class="meta-item">
          <IconFa name="check-circle" class="meta-icon" />
          <div class="meta-content">
            <span class="meta-label">Подтверждений</span>
            <span class="meta-value">{{ problem.confirmations_count || 0 }} чел.</span>
          </div>
        </div>
        <div class="meta-item">
          <IconFa name="star" class="meta-icon" />
          <div class="meta-content">
            <span class="meta-label">Рейтинг</span>
            <span class="meta-value">{{ (problem.rating || 0).toFixed(1) }}</span>
          </div>
        </div>
      </div>

      <!-- Галерея вложений (ИСПРАВЛЕНИЕ ЗАГРУЗКИ КАРТИНОК) -->
      <div v-if="problem.attachments && problem.attachments.length > 0" class="attachments-section">
        <h3 class="section-title">
          <IconFa name="images" class="me-2" /> Прикрепленные файлы ({{ problem.attachments.length }})
        </h3>
        <div class="attachments-grid">
          <div
              v-for="(attachment, index) in problem.attachments"
              :key="index"
              class="attachment-card"
              @click="openImagePreview(attachment)"
          >
            <img
                :src="getImageUrl(attachment.url || attachment.file_path)"
                :alt="attachment.name || 'Фото'"
                class="attachment-image"
                @error="handleImageError"
            >
            <div class="attachment-overlay">
              <IconFa name="search-plus" />
            </div>
          </div>
        </div>
      </div>

      <!-- История изменений (Timeline) -->
      <div class="timeline-section">
        <h3 class="section-title">
          <IconFa name="history" class="me-2" /> История изменений
        </h3>
        <ProblemTimeline :history="problem.status_history || []" />
      </div>

      <!-- Панель действий -->
      <div class="actions-bar">
        <button class="btn btn-primary" @click="openChat">
          <IconFa name="comments" class="me-2" /> Написать в чат
        </button>
        <button class="btn btn-outline" @click="downloadDocx">
          <IconFa name="file-word" class="me-2" /> Скачать отчет (DOCX)
        </button>
        <button v-if="canConfirm" class="btn btn-success" @click="confirmProblem">
          <IconFa name="check" class="me-2" /> Подтвердить решение
        </button>
      </div>
    </div>
  </AppPageContainer>

  <!-- Модальное окно предпросмотра изображения -->
  <div v-if="previewImage" class="image-preview-modal" @click.self="previewImage = null">
    <button class="close-preview" @click="previewImage = null">
      <IconFa name="times" />
    </button>
    <img :src="previewImage" alt="Preview" class="preview-img">
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProblemsStore } from '@/stores/problems.store'
import { useAuth } from '@/composables/useAuth'

import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import ProblemStatusBadge from '@/components/problems/ProblemStatusBadge.vue'
import ProblemTimeline from '@/components/problems/ProblemTimeline.vue'

const route = useRoute()
const router = useRouter()
const problemsStore = useProblemsStore()
const { isAuthenticated } = useAuth()

const problem = ref(null)
const isLoading = ref(true)
const previewImage = ref(null)

// Базовый URL бэкенда для корректной загрузки картинок
// Замените на ваш реальный URL, если он отличается
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const canConfirm = computed(() => {
  return isAuthenticated.value && !['resolved', 'closed', 'rejected'].includes(problem.value?.status)
})

onMounted(async () => {
  await loadProblem()
})

async function loadProblem() {
  isLoading.value = true
  try {
    // Убедитесь, что ваш store возвращает объект проблемы, а не просто массив
    problem.value = await problemsStore.fetchProblem(route.params.id)
  } catch (error) {
    console.error('Failed to load problem:', error)
    problem.value = null
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 🔥 ГЛАВНОЕ ИСПРАВЛЕНИЕ ДЛЯ КАРТИНОК 🔥
function getImageUrl(path) {
  if (!path) return ''
  // Если путь уже абсолютный (начинается с http), возвращаем как есть
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  // Иначе добавляем базовый URL бэкенда
  // Убираем слэш в начале пути, чтобы не было двойных слэшей (http://...//uploads)
  const cleanPath = path.startsWith('/') ? path.slice(1) : path
  return `${API_BASE_URL}/${cleanPath}`
}

function handleImageError(event) {
  // Если картинка не загрузилась, показываем заглушку
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiNlOGVkZjAiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9ImFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjNzA4MDhjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+0J/RgNC+0YHQutC+0LUg0L7QsdC70LDRgdGC0Yw8L3RleHQ+PC9zdmc+'
}

function openImagePreview(attachment) {
  previewImage.value = getImageUrl(attachment.url || attachment.file_path)
}

function openChat() {
  router.push({ name: 'ProblemChat', params: { id: route.params.id } })
}


async function downloadDocx() {
  if (!problem.value?.id) {
    alert('Не удалось определить номер обращения')
    return
  }

  try {
    const response = await problemsStore.downloadReport(
        problem.value.id
    )

    const blob = response?.data

    if (!(blob instanceof Blob) || blob.size === 0) {
      throw new Error('Сервер вернул пустой файл')
    }

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = url
    link.download = `otchet-po-obrashcheniyu-${problem.value.id}.docx`

    document.body.appendChild(link)
    link.click()
    link.remove()

    setTimeout(() => URL.revokeObjectURL(url), 1000)
  } catch (error) {
    console.error('[ProblemDetails] Ошибка скачивания отчёта:', error)

    const detail = error.response?.data

    if (detail instanceof Blob) {
      try {
        const text = await detail.text()
        const parsed = JSON.parse(text)
        alert(parsed.detail || 'Не удалось сформировать отчёт')
        return
      } catch {
        // Ответ не является JSON — показываем общее сообщение.
      }
    }

    alert(
        error.response?.status === 404
            ? 'Обращение не найдено на сервере'
            : 'Не удалось скачать отчёт. Проверьте соединение с сервером.'
    )
  }
}


async function confirmProblem() {
  if (!confirm('Вы уверены, что проблема решена удовлетворительно?')) return

  try {
    await problemsStore.confirmProblem(route.params.id)
    await loadProblem() // Перезагружаем данные для обновления статуса
  } catch (error) {
    console.error('Failed to confirm problem:', error)
    alert('Не удалось подтвердить решение. Попробуйте позже.')
  }
}
</script>

<style scoped>
/* === Дизайн-система === */
.problem-details {
  --ink: #172f40;
  --muted: #70808c;
  --line: #e8edf0;
  --accent: #00a896;
  --bg: #f8fafc;

  max-width: 800px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === Состояния === */
.loading-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--muted, #70808c);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--line, #e8edf0);
  border-top-color: var(--accent, #00a896);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

/* === Шапка === */
.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.badges-group {
  display: flex;
  gap: 0.5rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
}

.badge.badge-danger {
  background: rgba(198, 71, 82, 0.12);
  color: #c64752;
}

.badge.badge-warning {
  background: rgba(253, 126, 20, 0.12);
  color: #fd7e14;
}

.problem-id {
  font-size: 0.85rem;
  color: var(--muted, #70808c);
  font-weight: 600;
  background: var(--bg, #f8fafc);
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
}

/* === Контент === */
.problem-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--ink, #172f40);
  margin: 0 0 1rem;
  line-height: 1.3;
}

.problem-description {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #334155;
  margin-bottom: 2rem;
  white-space: pre-wrap;
}

/* === Мета-карточка === */
.meta-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  background: #fff;
  border: 1px solid var(--line, #e8edf0);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.meta-icon {
  color: var(--accent, #00a896);
  font-size: 1.1rem;
  margin-top: 0.15rem;
}

.meta-label {
  display: block;
  font-size: 0.78rem;
  color: var(--muted, #70808c);
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.meta-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink, #172f40);
}

/* === Вложения (Галерея) === */
.attachments-section {
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--ink, #172f40);
  margin: 0 0 1rem;
  display: flex;
  align-items: center;
}

.attachments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.attachment-card {
  position: relative;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--line, #e8edf0);
  transition: all 0.2s ease;
}

.attachment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(23, 47, 64, 0.1);
}

.attachment-card:hover .attachment-overlay {
  opacity: 1;
}

.attachment-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.attachment-overlay {
  position: absolute;
  inset: 0;
  background: rgba(23, 47, 64, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

/* === Действия === */
.actions-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--line, #e8edf0);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn.btn-primary {
  background: linear-gradient(135deg, var(--accent, #00a896), #087e8b);
  color: #fff;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
}

.btn.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
}

.btn.btn-success {
  background: linear-gradient(135deg, #06d6a0, #05b88a);
  color: #fff;
  box-shadow: 0 4px 12px rgba(6, 214, 160, 0.25);
}

.btn.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35);
}

.btn.btn-outline {
  background: #fff;
  border: 1px solid var(--line, #e8edf0);
  color: var(--ink, #172f40);
}

.btn.btn-outline:hover {
  border-color: var(--accent, #00a896);
  color: var(--accent, #00a896);
  background: rgba(0, 168, 150, 0.04);
}

/* === Предпросмотр изображения === */
.image-preview-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: fadeIn 0.2s ease;
}

.preview-img {
  max-width: 90%;
  max-height: 90vh;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.close-preview {
  position: absolute;
  top: 2rem;
  right: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.close-preview:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 575.98px) {
  .problem-title { font-size: 1.4rem; }
  .meta-card { grid-template-columns: 1fr 1fr; gap: 1rem; padding: 1rem; }
  .actions-bar { flex-direction: column; }
  .btn { width: 100%; }
}
</style>