<!-- client/src/views/auth/LoginView.vue -->
<!-- client/src/views/auth/LoginView.vue -->
<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Header -->
      <div class="auth-header">
        <div class="auth-brand-mark">
          <IconFa name="shield-halved" size="1.5rem" color="white" />
        </div>
        <h2>Вход в систему</h2>
        <p>Добро пожаловать обратно в Город под контролем</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="auth-form">
        <!-- Email -->
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <div class="input-wrapper" :class="{ 'is-invalid': errors.email }">
            <span class="input-icon">
              <IconFa name="envelope" />
            </span>
            <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-control-custom"
                placeholder="your@email.com"
                required
            >
          </div>
          <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password" class="form-label">Пароль</label>
          <div class="input-wrapper" :class="{ 'is-invalid': errors.password }">
            <span class="input-icon">
              <IconFa name="lock" />
            </span>
            <input
                id="password"
                v-model="form.password"
                type="password"
                class="form-control-custom"
                placeholder="Введите пароль"
                required
            >
          </div>
          <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
        </div>

        <!-- Error Alert -->
        <div v-if="loginError" class="alert-custom">
          <IconFa name="circle-exclamation" class="me-2" />
          {{ loginError }}
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn-custom-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <!-- Footer -->
      <div class="auth-footer">
        <router-link to="/forgot-password" class="link-muted">
          Забыли пароль?
        </router-link>

        <div class="divider"><span>или</span></div>

        <router-link to="/register" class="btn-custom-outline">
          Зарегистрироваться
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'LoginView',
  components: { IconFa },
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      errors: {},
      loginError: '',
      isLoading: false,
      // Инициализируем composable здесь, чтобы он был доступен в методах
      auth: useAuth()
    }
  },
  methods: {
    async handleLogin() {
      this.errors = {}
      this.loginError = ''

      if (!this.form.email) {
        this.errors.email = 'Введите email'
        return
      }
      if (!this.form.password) {
        this.errors.password = 'Введите пароль'
        return
      }

      this.isLoading = true

      try {
        // Вызываем login через инициализированный в data() composable
        const success = await this.auth.login(this.form.email, this.form.password)

        if (success) {
          // Используем this.$router для перенаправления с учетом query параметра
          const redirect = this.$route.query.redirect || '/profile'
          await this.$router.push(redirect)
        } else {
          this.loginError = 'Неверный email или пароль'
        }
      } catch (error) {
        // Показываем реальную ошибку с бэкенда, если она есть
        this.loginError = error.response?.data?.detail || 'Ошибка входа. Попробуйте позже.'
        console.error('Login error:', error)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;

  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 21px;
  padding: 2.5rem;
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.06);
}

/* Header */
.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-brand-mark {
  display: inline-flex;
  width: 56px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  margin-bottom: 1.25rem;
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.25);
}

.auth-header h2 {
  margin: 0;
  color: var(--layout-ink);
  font-size: 1.65rem;
  font-weight: 800;
  letter-spacing: -0.035em;
}

.auth-header p {
  margin: 0.5rem 0 0;
  color: var(--layout-muted);
  font-size: 0.95rem;
}

/* Form Elements - НОВЫЙ НАДЁЖНЫЙ ПОДХОД */
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.45rem;
  color: var(--layout-ink);
  font-size: 0.88rem;
  font-weight: 700;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: #fcfcfd;
  transition: all 180ms ease;
  overflow: hidden; /* Чтобы скругление не ломалось */
}

.input-wrapper:focus-within {
  border-color: var(--layout-accent);
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
}

.input-wrapper.is-invalid {
  border-color: #c64752;
  background: #fff0f1;
}

.input-wrapper.is-invalid:focus-within {
  box-shadow: 0 0 0 4px rgba(198, 71, 82, 0.1);
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px; /* Фиксированная ширина для идеального выравнивания */
  flex-shrink: 0;
  color: var(--layout-muted);
  transition: color 180ms ease;
}

.input-wrapper:focus-within .input-icon {
  color: var(--layout-accent);
}

.input-wrapper.is-invalid .input-icon {
  color: #c64752;
}

.form-control-custom {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.85rem 1rem 0.85rem 0;
  color: var(--layout-ink);
  font-size: 0.95rem;
  width: 100%;
}

.form-control-custom:focus {
  outline: none;
  box-shadow: none;
}

.form-control-custom::placeholder {
  color: #aab5bc;
}

.error-message {
  margin-top: 0.4rem;
  color: #c64752;
  font-size: 0.82rem;
  font-weight: 600;
}

/* Alert */
.alert-custom {
  display: flex;
  align-items: center;
  padding: 0.85rem 1rem;
  margin-bottom: 1.5rem;
  border-radius: 12px;
  background: #fff0f1;
  border: 1px solid rgba(198, 71, 82, 0.2);
  color: #c64752;
  font-size: 0.88rem;
  font-weight: 600;
}

/* Buttons */
.btn-custom-primary {
  width: 100%;
  padding: 0.95rem;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-size: 1rem;
  font-weight: 750;
  cursor: pointer;
  transition: all 180ms ease;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.25);
}

.btn-custom-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 168, 150, 0.35);
}

.btn-custom-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Footer */
.auth-footer {
  margin-top: 2rem;
  text-align: center;
}

.link-muted {
  color: var(--layout-muted);
  font-size: 0.88rem;
  text-decoration: none;
  font-weight: 600;
  transition: color 180ms ease;
}

.link-muted:hover {
  color: var(--layout-accent);
}

.divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
  color: var(--layout-muted);
  font-size: 0.82rem;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--layout-line);
}

.divider span {
  padding: 0 1rem;
}

.btn-custom-outline {
  display: block;
  width: 100%;
  padding: 0.85rem;
  border: 1px solid var(--layout-line);
  border-radius: 14px;
  background: transparent;
  color: var(--layout-ink);
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  text-align: center;
  transition: all 180ms ease;
}

.btn-custom-outline:hover {
  border-color: var(--layout-accent);
  background: rgba(0, 168, 150, 0.04);
  color: var(--layout-accent);
}

/* Mobile Adaptations */
@media (max-width: 575.98px) {
  .auth-container {
    min-height: calc(100vh - 150px);
    padding: 1.5rem 1rem;
  }

  .auth-card {
    padding: 1.75rem 1.25rem;
    border-radius: 18px;
  }

  .auth-header h2 {
    font-size: 1.45rem;
  }
}
</style>