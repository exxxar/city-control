<!-- client/src/views/auth/ResetPasswordView.vue -->
<template>

    <div class="reset-password-form">
      <h3 class="text-center mb-4">Новый пароль</h3>

      <form @submit.prevent="handleSubmit">
        <UiInput
          v-model="password"
          label="Новый пароль"
          type="password"
          placeholder="Минимум 6 символов"
          :error="errors.password"
          prepend-icon="bi-lock"
          required
        />

        <UiInput
          v-model="passwordConfirm"
          label="Подтвердите пароль"
          type="password"
          placeholder="Повторите пароль"
          :error="errors.passwordConfirm"
          prepend-icon="bi-lock-fill"
          required
        />

        <UiButton type="submit" variant="primary" :loading="isLoading" block>
          Сменить пароль
        </UiButton>
      </form>
    </div>

</template>

<script>
import AuthLayout from '@/layouts/AuthLayout.vue'
import UiInput from '@/components/ui/UiInput.vue'
import UiButton from '@/components/ui/UiButton.vue'

export default {
  name: 'ResetPasswordView',
  components: { AuthLayout, UiInput, UiButton },
  data() {
    return {
      password: '',
      passwordConfirm: '',
      errors: {},
      isLoading: false
    }
  },
  methods: {
    async handleSubmit() {
      this.errors = {}

      if (this.password.length < 6) {
        this.errors.password = 'Пароль должен быть не менее 6 символов'
        return
      }
      if (this.password !== this.passwordConfirm) {
        this.errors.passwordConfirm = 'Пароли не совпадают'
        return
      }

      this.isLoading = true
      try {
        // TODO: Реализовать API для сброса пароля
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('Пароль успешно изменен')
        this.$router.push('/login')
      } catch (error) {
        console.error('Reset password error:', error)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>