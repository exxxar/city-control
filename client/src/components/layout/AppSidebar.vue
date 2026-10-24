<!-- client/src/components/layout/AppSidebar.vue -->
<template>
  <aside class="app-sidebar bg-white border-end shadow-sm d-none d-md-flex flex-column">
    <!-- Logo -->
    <div class="sidebar-header p-3 border-bottom">
      <router-link to="/" class="d-flex align-items-center text-decoration-none">
        <IconFa name="shield-check" size="1.75rem" color="var(--civic-primary, #00A896)" />
        <span class="fw-bold text-dark ms-2">Город ПК</span>
      </router-link>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav flex-grow-1 py-3">
      <ul class="nav flex-column px-2">
        <li class="nav-item">
          <router-link to="/" class="nav-link d-flex align-items-center" active-class="active">
            <IconFa name="map" size="1.25rem" />
            <span class="ms-3">Карта</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/problems" class="nav-link d-flex align-items-center" active-class="active">
            <IconFa name="list-check" size="1.25rem" />
            <span class="ms-3">Обращения</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/initiatives" class="nav-link d-flex align-items-center" active-class="active">
            <IconFa name="lightbulb" size="1.25rem" />
            <span class="ms-3">Инициативы</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/events" class="nav-link d-flex align-items-center" active-class="active">
            <IconFa name="calendar-event" size="1.25rem" />
            <span class="ms-3">Мероприятия</span>
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/notifications" class="nav-link d-flex align-items-center position-relative" active-class="active">
            <IconFa name="bell" size="1.25rem" />
            <span class="ms-3">Уведомления</span>
            <span v-if="unreadCount > 0" class="badge bg-danger ms-auto">{{ unreadCount }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Create button -->
    <div class="sidebar-footer p-3 border-top">
      <router-link to="/create" class="btn btn-civic w-100 d-flex align-items-center justify-content-center">
        <IconFa name="plus-lg" size="1.25rem" color="white" />
        <span class="ms-2 fw-bold">Сообщить</span>
      </router-link>
    </div>

    <!-- Profile -->
    <div class="sidebar-profile p-3 border-top">
      <router-link to="/profile" class="d-flex align-items-center text-decoration-none text-dark">
        <div class="profile-avatar bg-civic text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
          <IconFa name="person" size="1.25rem" />
        </div>
        <div class="ms-3 flex-grow-1">
          <div class="fw-bold small">{{ userName }}</div>
          <div class="text-muted" style="font-size: 0.7rem;">Профиль</div>
        </div>
        <IconFa name="chevron-right" size="0.875rem" color="#adb5bd" />
      </router-link>
    </div>
  </aside>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useNotificationsStore } from '@/stores/notifications.store'
import { useAuthStore } from '@/stores/auth.store'

export default {
  name: 'AppSidebar',
  components: { IconFa },
  computed: {
    notificationsStore() {
      return useNotificationsStore()
    },
    authStore() {
      return useAuthStore()
    },
    unreadCount() {
      return this.notificationsStore.unreadCount
    },
    userName() {
      return this.authStore.user?.full_name || 'Пользователь'
    }
  }
}
</script>

<style scoped>
.app-sidebar {
  width: 260px;
  height: 100vh;
  position: sticky;
  top: 0;
  z-index: 1010;
}

.sidebar-nav .nav-link {
  color: #495057;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.25rem;
  transition: all 0.2s ease;
}

.sidebar-nav .nav-link:hover {
  background-color: #f8f9fa;
  color: var(--civic-primary, #00A896);
}

.sidebar-nav .nav-link.active {
  background-color: rgba(0, 168, 150, 0.1);
  color: var(--civic-primary, #00A896);
  font-weight: 600;
}

.sidebar-nav .nav-link .badge {
  font-size: 0.7rem;
  padding: 0.25em 0.5em;
}

.btn-civic {
  background: linear-gradient(135deg, #00A896, #007EA7);
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.3);
  transition: all 0.2s ease;
}

.btn-civic:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.4);
}

.profile-avatar {
  flex-shrink: 0;
}

.sidebar-profile a:hover .profile-avatar {
  background-color: #008f80;
}
</style>