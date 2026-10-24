<!-- client/src/App.vue -->
<template>
  <div id="app">
    <router-view />
    <UiToast ref="toast" />
  </div>
</template>

<script>
import UiToast from '@/components/ui/UiToast.vue'

export default {
  name: 'App',
  components: { UiToast },
  mounted() {
    // Инициализация offline-очереди
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.ready.then((registration) => {
        console.log('[App] Service Worker ready')
      })
    }
  }
}
</script>

<style>
/* Глобальные стили уже подключены в main.js */
</style>