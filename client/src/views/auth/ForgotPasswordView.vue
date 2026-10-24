<!-- client/src/views/auth/ForgotPasswordView.vue -->
<template>

    <div class="forgot-password-form">
      <h3 class="text-center mb-4">Восстановление пароля</h3>
      <p class="text-muted text-center mb-4">
        Введите email, и мы отправим ссылку для сброса пароля
      </p>

      <form @submit.prevent="handleSubmit">
        <UiInput
          v-model="email"
          label="Email"
          type="email"
          placeholder="your@email.com"
          :error="error"
          prepend-icon="bi-envelope"
          required
        />

        <UiButton type="submit" variant="primary" :loading="isLoading" block>
          Отправить ссылку
        </UiButton>
      </form>

      <div class="text-center mt-3">
        <router-link to="/login" class="text-muted">
          Вернуться ко входу
        </router-link>
      </div>
    </div>

</template>

<script>
import AuthLayout from '@/layouts/AuthLayout.vue'
import UiInput from '@/components/ui/UiInput.vue'
import UiButton from '@/components/ui/UiButton.vue'

export default {
  name: 'ForgotPasswordView',
  components: { AuthLayout, UiInput, UiButton },
  data() {
    return {
      email: '',
      error: '',
      isLoading: false
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true
      this.error = ''

      try {
        // TODO: Реализовать API для восстановления пароля
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('Ссылка для сброса пароля отправлена на ваш email')
        this.$router.push('/login')
      } catch (error) {
        this.error = 'Ошибка отправки. Попробуйте позже.'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>