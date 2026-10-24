<!-- client/src/views/profile/ProfileView.vue -->
<template>
  <AppPageContainer>
    <template #header>
      <div class="page-header-modern">
        <div>
          <h2 class="page-title">Мой профиль</h2>
          <p class="page-subtitle">Управляйте личными данными и настройками аккаунта</p>
        </div>
      </div>
    </template>

    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-border text-civic" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p class="text-muted small mt-3">Загружаем данные профиля...</p>
    </div>

    <!-- Основной контент -->
    <div v-else-if="user" class="profile-grid">

      <!-- Левая колонка: Информация о пользователе -->
      <div class="profile-info-card">
        <div class="avatar-wrapper">
          <div class="avatar-circle">
            <IconFa name="user" size="2.5rem" color="white" />
          </div>
          <span class="avatar-status"></span>
        </div>

        <h3 class="user-name">{{ user.full_name }}</h3>
        <p class="user-email">
          <IconFa name="envelope" class="me-1" size="0.85rem" />
          {{ user.email }}
        </p>

        <div class="user-roles">
          <span v-for="role in user.roles" :key="role.id" class="role-badge">
            <IconFa name="shield-halved" class="me-1" size="0.75rem" />
            {{ role.name }}
          </span>
        </div>

        <div class="info-divider"></div>

        <div class="quick-actions">
          <router-link to="/settings" class="action-link">
            <IconFa name="gear" class="me-2" />
            Настройки аккаунта
          </router-link>
          <button class="action-link action-link--danger" @click="logout">
            <IconFa name="right-from-bracket" class="me-2" />
            Выйти из системы
          </button>
        </div>
      </div>

      <!-- Правая колонка: Форма редактирования -->
      <div class="profile-form-card">
        <h4 class="form-title">Личные данные</h4>
        <p class="form-subtitle">Эта информация будет видна в ваших обращениях</p>

        <form @submit.prevent="updateProfile" class="edit-form">
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

          <!-- Сообщения об успехе/ошибке -->
          <div v-if="updateError" class="alert-custom">
            <IconFa name="circle-exclamation" class="me-2" />
            {{ updateError }}
          </div>

          <div v-if="updateSuccess" class="alert-custom alert-success-custom">
            <IconFa name="circle-check" class="me-2" />
            Профиль успешно обновлен
          </div>

          <!-- Кнопка сохранения -->
          <button type="submit" class="btn-custom-primary" :disabled="isUpdating">
            <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>
            {{ isUpdating ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </form>
      </div>

    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import IconFa from '@/components/ui/IconFa.vue'
import { useUserStore } from '@/stores/user.store'
import { useAuth } from '@/composables/useAuth'

export default {
  name: 'ProfileView',
  components: { AppPageContainer, IconFa },
  data() {
    return {
      form: {
        full_name: '',
        email: '',
        phone: ''
      },
      errors: {},
      updateError: '',
      updateSuccess: false,
      isUpdating: false
    }
  },
  computed: {
    userStore() {
      return useUserStore()
    },
    user() {
      return this.userStore.profile
    },
    isLoading() {
      return this.userStore.isLoading
    }
  },
  watch: {
    user: {
      handler(newUser) {
        if (newUser) {
          this.form.full_name = newUser.full_name
          this.form.email = newUser.email
          this.form.phone = newUser.phone || ''
        }
      },
      immediate: true
    }
  },
  async mounted() {
    if (!this.user) {
      await this.userStore.fetchProfile()
    }
  },
  methods: {
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

    async updateProfile() {
      this.errors = {}
      this.updateError = ''
      this.updateSuccess = false

      if (!this.form.full_name.trim() || this.form.full_name.trim().split(' ').length < 2) {
        this.errors.full_name = 'Введите Фамилию и Имя'
        return
      }
      if (!this.form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Введите корректный email'
        return
      }

      this.isUpdating = true
      try {
        const success = await this.userStore.updateProfile({
          full_name: this.form.full_name.trim(),
          email: this.form.email.trim().toLowerCase(),
          phone: this.form.phone
        })

        if (success) {
          this.updateSuccess = true
          setTimeout(() => { this.updateSuccess = false }, 4000)
        } else {
          this.updateError = this.userStore.error || 'Ошибка обновления профиля'
        }
      } catch (error) {
        this.updateError = error.response?.data?.detail || 'Ошибка обновления профиля'
        console.error('Update profile error:', error)
      } finally {
        this.isUpdating = false
      }
    },

    logout() {
      const { logout } = useAuth()
      logout()
    }
  }
}
</script>

<style scoped>
/* === Переменные дизайн-системы === */
.profile-grid {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: #00a896;

  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 992px) {
  .profile-grid {
    grid-template-columns: 320px 1fr;
    align-items: start;
  }
}

/* === Заголовок страницы === */
.page-header-modern {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--layout-ink);
  letter-spacing: -0.03em;
  margin: 0;
}

.page-subtitle {
  color: var(--layout-muted);
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

/* === Карточка информации (Левая) === */
.profile-info-card {
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 20px;
  padding: 2rem 1.5rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 1.25rem;
}

.avatar-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00a896, #087e8b);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.25);
}

.avatar-status {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 16px;
  height: 16px;
  background: #06D6A0;
  border: 3px solid #ffffff;
  border-radius: 50%;
}

.user-name {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.user-email {
  color: var(--layout-muted);
  font-size: 0.9rem;
  margin: 0 0 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-roles {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.75rem;
  background: rgba(0, 168, 150, 0.08);
  color: #008f80;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 700;
}

.info-divider {
  height: 1px;
  background: var(--layout-line);
  margin: 1.5rem 0;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-link {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 650;
  color: var(--layout-ink);
  background: #f8fafc;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.action-link:hover {
  background: #ffffff;
  border-color: var(--layout-line);
  color: var(--layout-accent);
}

.action-link--danger {
  color: #c64752;
}

.action-link--danger:hover {
  background: #fff0f1;
  border-color: rgba(198, 71, 82, 0.2);
}

/* === Карточка формы (Правая) === */
.profile-form-card {
  background: #ffffff;
  border: 1px solid var(--layout-line);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.form-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--layout-ink);
  margin: 0 0 0.25rem;
}

.form-subtitle {
  color: var(--layout-muted);
  font-size: 0.9rem;
  margin: 0 0 1.5rem;
}

/* === Стили формы (как в Login/Register) === */
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

/* === Алерты === */
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

.alert-success-custom {
  background: rgba(6, 214, 160, 0.1);
  border-color: rgba(6, 214, 160, 0.3);
  color: #059669;
}

/* === Кнопка === */
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

/* === Загрузка === */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
}

/* === Мобильная адаптация === */
@media (max-width: 575.98px) {
  .profile-form-card,
  .profile-info-card {
    padding: 1.5rem 1.25rem;
    border-radius: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }
}
</style>