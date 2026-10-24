// client/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth.store'
import { initPWA } from './sw/register-sw'

// Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

// Импорт CSS Font Awesome (обязательно!)
import '@fortawesome/fontawesome-svg-core/styles.css'

// Bootstrap 5 CSS и JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

// Leaflet CSS
import 'leaflet/dist/leaflet.css'

// Кастомные стили
import './assets/styles/tokens.css'
import './assets/styles/reset.css'
import './assets/styles/typography.css'
import './assets/styles/layout.css'
import './assets/styles/utilities.css'
import './assets/styles/animations.css'
import './assets/styles/main.css'

// === РЕГИСТРАЦИЯ ВСЕХ ИКОНОК FA ===
library.add(fas, far, fab)

const app = createApp(App)
const pinia = createPinia()

// Глобальная регистрация компонента <font-awesome-icon>
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(pinia)
app.use(router)

// Инициализируем пользователя при старте
const authStore = useAuthStore()
authStore.init().finally(() => {
  app.mount('#app')

  // Инициализируем PWA в продакшене
  if (import.meta.env.PROD) {
    initPWA()
  }
})