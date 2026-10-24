<!-- client/src/views/auth/RegisterView.vue -->
<template>

    <div class="auth-container">
      <div class="auth-card">
        <!-- Header -->
        <div class="auth-header">
          <div class="auth-brand-mark">
            <IconFa name="user-plus" size="1.5rem" color="white" />
          </div>
          <h2>Создать аккаунт</h2>
          <p>Присоединяйтесь к сообществу активного города</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegister" class="auth-form">
          <!-- ФИО -->
          <div class="form-group">
            <label for="fullName" class="form-label">ФИО</label>
            <div class="input-wrapper" :class="{ 'is-invalid': errors.full_name }">
              <span class="input-icon">
                <IconFa name="user" />
              </span>
              <input
                  id="fullName"
                  v-model="form.full_name"
                  type="text"
                  class="form-control-custom"
                  placeholder="Иванов Иван Иванович"
                  required
              >
            </div>
            <div v-if="errors.full_name" class="error-message">{{ errors.full_name }}</div>
          </div>

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

          <!-- Телефон -->
          <div class="form-group">
            <label for="phone" class="form-label">Телефон</label>
            <div class="input-wrapper" :class="{ 'is-invalid': errors.phone }">
              <span class="input-icon">
                <IconFa name="phone" />
              </span>
              <input
                  id="phone"
                  type="tel"
                  class="form-control-custom"
                  placeholder="+7 (___) ___-__-__"
                  :value="form.phone"
                  @input="formatPhone"
              >
            </div>
            <div v-if="errors.phone" class="error-message">{{ errors.phone }}</div>
          </div>

          <!-- Пароль -->
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
                  placeholder="Минимум 6 символов"
                  required
              >
            </div>
            <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
          </div>

          <!-- Подтверждение пароля -->
          <div class="form-group">
            <label for="passwordConfirm" class="form-label">Подтвердите пароль</label>
            <div class="input-wrapper" :class="{ 'is-invalid': errors.password_confirm }">
              <span class="input-icon">
                <IconFa name="lock" />
              </span>
              <input
                  id="passwordConfirm"
                  v-model="form.password_confirm"
                  type="password"
                  class="form-control-custom"
                  placeholder="Повторите пароль"
                  required
              >
            </div>
            <div v-if="errors.password_confirm" class="error-message">{{ errors.password_confirm }}</div>
          </div>

          <!-- Сообщение об ошибке API -->
          <div v-if="registerError" class="alert-custom">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ registerError }}
          </div>

          <!-- Кнопка регистрации -->
          <button type="submit" class="btn-custom-primary" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
            {{ isLoading ? 'Создание аккаунта...' : 'Зарегистрироваться' }}
          </button>
        </form>

        <!-- Footer -->
        <div class="auth-footer">
          <span class="text-muted">Уже есть аккаунт? </span>
          <router-link to="/login" class="link-accent fw-bold">
            Войти в систему
          </router-link>
        </div>
      </div>
    </div>

</template>

<script>
import AuthLayout from '@/layouts/AuthLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'
import * as authApi from '@/api/auth.api'

export default {
  name: 'RegisterView',
  components: { AuthLayout, IconFa },
  data() {
    return {
      form: {
        full_name: '',
        email: '',
        phone: '',
        password: '',
        password_confirm: ''
      },
      errors: {},
      registerError: '',
      isLoading: false
    }
  },
  methods: {
    // Нативная маска телефона
    formatPhone(e) {
      let val = e.target.value.replace(/\D/g, '')
      if (val.length > 0) {
        if (val[0] === '7' || val[0] === '8') val = val.substring(1)
        let formatted = '+7'
        if (val.length > 0) formatted += ' (' + val.substring(0, 3)
        if (val.length >= 3) formatted += ') ' + val.substring(3, 6)
        if (val.length >= 6) formatted += '-' + val.substring(6, 8)
        if (val.length >= 8) formatted += '-' + val.substring(8, 10)
        this.form.phone = formatted
      } else {
        this.form.phone = ''
      }
    },

    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.form.full_name.trim() || this.form.full_name.trim().split(' ').length < 2) {
        this.errors.full_name = 'Введите Фамилию и Имя'
        isValid = false
      }

      if (!this.form.email) {
        this.errors.email = 'Введите email'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Некорректный формат email'
        isValid = false
      }

      if (this.form.phone && this.form.phone.length < 18) {
        this.errors.phone = 'Введите корректный номер телефона'
        isValid = false
      }

      if (!this.form.password) {
        this.errors.password = 'Введите пароль'
        isValid = false
      } else if (this.form.password.length < 6) {
        this.errors.password = 'Пароль должен быть не менее 6 символов'
        isValid = false
      }

      if (this.form.password !== this.form.password_confirm) {
        this.errors.password_confirm = 'Пароли не совпадают'
        isValid = false
      }

      return isValid
    },

    async handleRegister() {
      if (!this.validateForm()) return

      this.isLoading = true
      this.registerError = ''

      try {
        await authApi.register({
          full_name: this.form.full_name.trim(),
          email: this.form.email.trim().toLowerCase(),
          phone: this.form.phone,
          password: this.form.password
        })

        // Успешная регистрация
        // Можно показать toast-уведомление, но пока используем alert или редирект
        this.$router.push({
          path: '/login',
          query: { registered: 'true' }
        })
      } catch (error) {
        this.registerError = error.response?.data?.detail || 'Ошибка регистрации. Попробуйте позже.'
        console.error('Register error:', error)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* Используем те же переменные, что и в LoginView для единообразия */
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
  max-width: 480px;
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

/* Form Elements */
.form-group {
  margin-bottom: 1.15rem;
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
  overflow: hidden;
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
  width: 48px;
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
  margin-top: 0.5rem;
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
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
}

.link-accent {
  color: var(--layout-accent);
  text-decoration: none;
  transition: color 180ms ease;
}

.link-accent:hover {
  color: #008f80;
  text-decoration: underline;
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