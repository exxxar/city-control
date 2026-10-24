<!-- admin/src/components/notifications/NotificationsDropdown.vue -->
<template>
  <div class="notifications-dropdown" ref="dropdown">
    <button class="notifications-btn" @click="toggleDropdown">
      <i class="fas fa-bell"></i>
      <span v-if="notificationsStore.unreadCount > 0" class="badge">
        {{ notificationsStore.unreadCount }}
      </span>
    </button>

    <Transition name="fade">
      <div v-if="isOpen" class="dropdown-panel">
        <div class="dropdown-header">
          <h3>Уведомления</h3>
          <button v-if="notificationsStore.unreadCount > 0" class="mark-all-btn" @click="markAllAsRead">
            Прочитать все
          </button>
        </div>

        <div class="dropdown-body">
          <div v-if="notificationsStore.isLoading" class="loading-state">
            <div class="spinner-small"></div>
          </div>

          <div v-else-if="notificationsStore.items.length === 0" class="empty-state">
            <i class="fas fa-bell-slash"></i>
            <p>Нет уведомлений</p>
          </div>

          <div v-else class="notifications-list">
            <div
                v-for="notification in notificationsStore.items"
                :key="notification.id"
                class="notification-item"
                :class="{ unread: !notification.is_read }"
                @click="handleNotificationClick(notification)"
            >
              <div class="notification-icon" :style="{ background: notification.color + '20', color: notification.color }">
                <i :class="`fas ${notification.icon}`"></i>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
              </div>
              <div v-if="!notification.is_read" class="unread-dot"></div>
            </div>
          </div>
        </div>

        <div class="dropdown-footer">
          <router-link to="/notifications" class="view-all-link">
            Все уведомления
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationsStore } from '@/stores/notifications.store'

const router = useRouter()
const notificationsStore = useNotificationsStore()

const isOpen = ref(false)
const dropdown = ref(null)

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function handleClickOutside(event) {
  if (dropdown.value && !dropdown.value.contains(event.target)) {
    isOpen.value = false
  }
}

function handleNotificationClick(notification) {
  if (!notification.is_read) {
    notificationsStore.markAsRead(notification.id)
  }
  if (notification.link) {
    router.push(notification.link)
    isOpen.value = false
  }
}

async function markAllAsRead() {
  await notificationsStore.markAllAsRead()
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))

  if (diffMins < 1) return 'только что'
  if (diffMins < 60) return `${diffMins} мин. назад`
  if (diffHours < 24) return `${diffHours} ч. назад`
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

onMounted(() => {
  notificationsStore.fetchNotifications()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped lang="scss">
.notifications-dropdown { position: relative; }

.notifications-btn {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid #e8edf0;
  background: white;
  color: #70808c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;

  &:hover {
    background: #f8fafc;
    color: #00a896;
    border-color: #00a896;
  }
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #c64752;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(198, 71, 82, 0.3);
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 380px;
  background: white;
  border: 1px solid #e8edf0;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e8edf0;

  h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 800;
    color: #172f40;
  }
}

.mark-all-btn {
  background: none;
  border: none;
  color: #00a896;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s ease;

  &:hover {
    color: #008f80;
  }
}

.dropdown-body {
  max-height: 400px;
  overflow-y: auto;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.spinner-small {
  width: 24px;
  height: 24px;
  border: 2px solid #e8edf0;
  border-top-color: #00a896;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #70808c;

  i {
    font-size: 2rem;
    opacity: 0.3;
    margin-bottom: 0.5rem;
  }

  p {
    margin: 0;
    font-size: 0.88rem;
  }
}

.notifications-list {
  padding: 0.5rem 0;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.85rem 1.25rem;
  cursor: pointer;
  transition: background 0.15s ease;
  position: relative;

  &:hover {
    background: #f8fafc;
  }

  &.unread {
    background: rgba(0, 168, 150, 0.03);
  }

  & + & {
    border-top: 1px solid #f1f5f9;
  }
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 700;
  color: #172f40;
  font-size: 0.88rem;
  margin-bottom: 0.25rem;
}

.notification-message {
  color: #70808c;
  font-size: 0.82rem;
  line-height: 1.4;
  margin-bottom: 0.35rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-time {
  color: #aab5bc;
  font-size: 0.75rem;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #00a896;
  flex-shrink: 0;
  align-self: center;
}

.dropdown-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #e8edf0;
  text-align: center;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #00a896;
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  transition: gap 0.2s ease;

  &:hover {
    gap: 0.75rem;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 480px) {
  .dropdown-panel {
    width: calc(100vw - 2rem);
    right: -1rem;
  }
}
</style>