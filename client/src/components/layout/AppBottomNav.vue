<!-- client/src/components/layout/AppBottomNav.vue -->
<template>
  <nav class="app-bottom-nav">
    <div class="nav-items">
      <router-link to="/" class="nav-item" active-class="active">
        <IconFa name="map" size="1.4rem" />
        <span>Карта</span>
      </router-link>

      <router-link to="/problems" class="nav-item" active-class="active">
        <IconFa name="list-check" size="1.4rem" />
        <span>Обращения</span>
      </router-link>

      <!-- Центральная кнопка "Сообщить" -->
      <router-link to="/create" class="nav-item create-btn-wrapper">
        <div class="create-btn">
          <IconFa name="plus-lg" size="1.6rem" color="white" />
        </div>
        <span class="create-label">Сообщить</span>
      </router-link>

      <router-link to="/notifications" class="nav-item position-relative" active-class="active">
        <IconFa name="bell" size="1.4rem" />
        <span v-if="unreadCount > 0" class="badge-notif">
          {{ unreadCount > 9 ? '9+' : unreadCount }}
        </span>
        <span>Алерты</span>
      </router-link>

      <router-link to="/profile" class="nav-item" active-class="active">
        <IconFa name="person" size="1.4rem" />
        <span>Профиль</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useNotificationsStore } from '@/stores/notifications.store'

export default {
  name: 'AppBottomNav',
  components: { IconFa },
  computed: {
    notificationsStore() {
      return useNotificationsStore()
    },
    unreadCount() {
      return this.notificationsStore.unreadCount
    }
  }
}
</script>

<style scoped>
.app-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e9ecef;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 1020;
  padding-bottom: env(safe-area-inset-bottom);
}

.nav-items {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.5rem 0;
  max-width: 600px;
  margin: 0 auto;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #6c757d;
  font-size: 0.7rem;
  padding: 0.5rem;
  min-width: 60px;
  transition: color 0.2s;
  -webkit-tap-highlight-color: transparent;
}

.nav-item.active {
  color: var(--civic-primary, #00A896);
}

.nav-item span {
  margin-top: 0.25rem;
  font-weight: 500;
}

/* Центральная кнопка "Сообщить" */
.create-btn-wrapper {
  position: relative;
  margin-top: -1.5rem;
}

.create-btn {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #00A896, #007EA7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.4);
  transition: transform 0.2s;
}

.create-btn:active {
  transform: scale(0.95);
}

.create-label {
  color: var(--civic-primary, #00A896);
  font-weight: 600;
  margin-top: 0.25rem;
}

/* Бейдж уведомлений */
.badge-notif {
  position: absolute;
  top: 0;
  right: 8px;
  background: #EF476F;
  color: white;
  border-radius: 50%;
  min-width: 18px;
  height: 18px;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 2px solid white;
  padding: 0 4px;
}

/* Для очень маленьких экранов (< 360px) */
@media (max-width: 360px) {
  .nav-item {
    min-width: 50px;
    font-size: 0.65rem;
  }

  .create-btn {
    width: 48px;
    height: 48px;
  }
}
</style>