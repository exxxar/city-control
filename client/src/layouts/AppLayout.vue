<!-- client/src/layouts/AppLayout.vue -->
<template>
  <div class="app-layout">
    <!-- Sidebar для desktop (скрыт на мобильных) -->
    <AppSidebar class="d-none d-md-flex" />

    <!-- Main content area -->
    <div class="main-wrapper">
      <!-- Header для mobile (скрыт на desktop) -->
      <AppHeader class="d-md-none" />

      <!-- Page content -->
      <main class="main-content">
        <router-view />
      </main>

      <!-- Bottom nav для mobile (скрыт на desktop) -->
      <AppBottomNav class="d-md-none" />
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppBottomNav from '@/components/layout/AppBottomNav.vue'

export default {
  name: 'AppLayout',
  components: {
    AppHeader,
    AppSidebar,
    AppBottomNav
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background-color: #f8f9fa;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
  position: relative;
}

.main-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* На мобильных: header + content + bottom nav */
@media (max-width: 767.98px) {
  .main-content {
    /* Высота = 100% - header(~60px) - bottom nav(~70px) */
    height: calc(100% - 130px);
  }
}

/* На десктопе: sidebar + content */
@media (min-width: 768px) {
  .main-content {
    height: 100%;
  }
}
</style>