<!-- admin/src/views/auth/LoginView.vue -->
<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Заголовок -->
      <div class="login-header">
        <div class="brand-mark">
          <i class="fas fa-shield-halved"></i>
        </div>
        <h1>Админ-панель</h1>
        <p class="subtitle">Город под контролем</p>
      </div>

      <!-- Форма -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Email -->
        <div class="form-group">
          <label class="form-label">Email</label>
          <div class="input-wrapper" :class="{ 'is-invalid': errors.email }">
            <span class="input-icon">
              <i class="fas fa-envelope"></i>
            </span>
            <input
                v-model="form.email"
                type="email"
                class="form-control-custom"
                placeholder="admin@city.local"
                autocomplete="email"
                required
            >
          </div>
          <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label class="form-label">Пароль</label>
          <div class="input-wrapper" :class="{ 'is-invalid': errors.password }">
            <span class="input-icon">
              <i class="fas fa-lock"></i>
            </span>
            <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-control-custom"
                placeholder="Введите пароль"
                autocomplete="current-password"
                required
            >
            <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
                tabindex="-1"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
        </div>

        <!-- Глобальная ошибка -->
        <Transition name="fade">
          <div v-if="loginError" class="error-banner">
            <i class="fas fa-circle-exclamation"></i>
            <span>{{ loginError }}</span>
          </div>
        </Transition>

        <!-- Кнопка -->
        <button type="submit" class="btn-submit" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          <i v-else class="fas fa-right-to-bracket"></i>
          <span>{{ isLoading ? 'Вход...' : 'Войти в систему' }}</span>
        </button>
      </form>

      <!-- Футер -->
      <div class="login-footer">
        <router-link to="/" class="back-link">
          <i class="fas fa-arrow-left"></i>
          Вернуться на сайт
        </router-link>
      </div>
    </div>

    <!-- Фоновые декорации -->
    <div class="bg-decoration bg-decoration--1"></div>
    <div class="bg-decoration bg-decoration--2"></div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const loginError = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

async function handleLogin() {
  // Сбрасываем ошибки
  errors.email = ''
  errors.password = ''
  loginError.value = ''
  authStore.clearError()

  // Валидация
  let isValid = true

  if (!form.email.trim()) {
    errors.email = 'Введите email'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Некорректный email'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Введите пароль'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Пароль слишком короткий'
    isValid = false
  }

  if (!isValid) return

  isLoading.value = true
  try {
    await authStore.login(form.email, form.password)

    // Редирект на страницу, с которой пришли, или на дашборд
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (error) {
    loginError.value = error.message || 'Неверный email или пароль'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(135deg, #172f40 0%, #0f1f2b 100%);
  position: relative;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  pointer-events: none;

  &--1 {
    width: 400px;
    height: 400px;
    background: #00a896;
    top: -100px;
    right: -100px;
  }

  &--2 {
    width: 500px;
    height: 500px;
    background: #087e8b;
    bottom: -150px;
    left: -150px;
  }
}

.login-card {
  position: relative;
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-size: 1.75rem;
  margin-bottom: 1rem;
  box-shadow: 0 8px 24px rgba(0, 168, 150, 0.35);
}

.login-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
}

.subtitle {
  margin: 0.5rem 0 0;
  color: #70808c;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  display: block;
  margin-bottom: 0.45rem;
  color: #172f40;
  font-size: 0.88rem;
  font-weight: 700;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #e8edf0;
  border-radius: 14px;
  background: #fcfcfd;
  transition: all 180ms ease;
  overflow: hidden;

  &:focus-within {
    border-color: #00a896;
    background: white;
    box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
  }

  &.is-invalid {
    border-color: #c64752;
    background: #fff0f1;
  }
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  flex-shrink: 0;
  color: #70808c;
  transition: color 180ms ease;

  .input-wrapper:focus-within & {
    color: #00a896;
  }

  .input-wrapper.is-invalid & {
    color: #c64752;
  }
}

.form-control-custom {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.85rem 1rem 0.85rem 0;
  color: #172f40;
  font-size: 0.95rem;
  width: 100%;
  outline: none;

  &::placeholder {
    color: #aab5bc;
  }
}

.password-toggle {
  background: transparent;
  border: none;
  padding: 0 1rem;
  color: #70808c;
  cursor: pointer;
  transition: color 180ms ease;

  &:hover {
    color: #00a896;
  }
}

.error-message {
  margin-top: 0.4rem;
  color: #c64752;
  font-size: 0.82rem;
  font-weight: 600;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border-radius: 12px;
  background: #fff0f1;
  border: 1px solid rgba(198, 71, 82, 0.2);
  color: #c64752;
  font-size: 0.88rem;
  font-weight: 600;

  i {
    font-size: 1.1rem;
  }
}

.btn-submit {
  width: 100%;
  padding: 0.95rem;
  margin-top: 0.5rem;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-size: 1rem;
  font-weight: 750;
  cursor: pointer;
  transition: all 180ms ease;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0, 168, 150, 0.35);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #70808c;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 180ms ease;

  &:hover {
    color: #00a896;
  }
}

/* Анимации */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Адаптивность */
@media (max-width: 480px) {
  .login-card {
    padding: 2rem 1.5rem;
    border-radius: 20px;
  }

  .login-header h1 {
    font-size: 1.5rem;
  }

  .brand-mark {
    width: 56px;
    height: 56px;
    font-size: 1.5rem;
  }
}
</style>