<!-- client/src/components/layout/AppHeader.vue -->
<template>
  <header class="app-header bg-white border-bottom shadow-sm sticky-top">
    <div class="container-fluid px-3 py-2">
      <div class="d-flex align-items-center justify-content-between">
        <!-- Logo -->
        <router-link to="/" class="d-flex align-items-center text-decoration-none">
          <IconFa name="shield-check" size="1.5rem" color="var(--civic-primary, #00A896)" />
          <span class="fw-bold text-dark ms-2 d-none d-sm-inline">Город под контролем</span>
        </router-link>

        <!-- Right actions -->
        <div class="d-flex align-items-center gap-2">
          <!-- Notifications -->
          <router-link to="/notifications" class="position-relative text-secondary p-2 rounded-circle hover-bg">
            <IconFa name="bell" size="1.25rem" />
            <span v-if="unreadCount > 0" class="badge-notif">
              {{ unreadCount > 9 ? '9+' : unreadCount }}
            </span>
          </router-link>

          <!-- Profile -->
          <router-link to="/profile" class="text-secondary p-2 rounded-circle hover-bg">
            <IconFa name="person-circle" size="1.25rem" />
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useNotificationsStore } from '@/stores/notifications.store'

export default {
  name: 'AppHeader',
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
.app-header {
  z-index: 1020;
}

.hover-bg:hover {
  background-color: #f8f9fa;
}

.badge-notif {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #EF476F;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 2px solid white;
}
</style>