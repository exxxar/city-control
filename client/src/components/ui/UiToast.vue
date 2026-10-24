<!-- client/src/components/ui/UiToast.vue -->
<template>
  <Teleport to="body">
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1100">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', toast.show ? 'show' : '', toastClass(toast)]"
          role="alert"
        >
          <div class="toast-header">
            <i v-if="toast.icon" :class="toast.icon" class="me-2"></i>
            <strong class="me-auto">{{ toast.title }}</strong>
            <small class="text-muted">{{ toast.time }}</small>
            <button
              type="button"
              class="btn-close"
              @click="remove(toast.id)"
            ></button>
          </div>
          <div v-if="toast.message" class="toast-body">
            {{ toast.message }}
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script>
export default {
  name: 'UiToast',
  data() {
    return {
      toasts: []
    }
  },
  methods: {
    show(options) {
      const toast = {
        id: Date.now() + Math.random(),
        title: options.title || 'Уведомление',
        message: options.message || '',
        variant: options.variant || 'info',
        icon: options.icon || '',
        time: new Date().toLocaleTimeString(),
        show: true,
        duration: options.duration || 5000
      }

      this.toasts.push(toast)

      if (toast.duration > 0) {
        setTimeout(() => {
          this.remove(toast.id)
        }, toast.duration)
      }
    },
    remove(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index !== -1) {
        this.toasts[index].show = false
        setTimeout(() => {
          this.toasts = this.toasts.filter(t => t.id !== id)
        }, 300)
      }
    },
    toastClass(toast) {
      return {
        'border-success': toast.variant === 'success',
        'border-danger': toast.variant === 'danger',
        'border-warning': toast.variant === 'warning',
        'border-info': toast.variant === 'info'
      }
    }
  }
}
</script>

<style scoped>
.toast {
  border-radius: 8px;
  margin-bottom: 0.5rem;
  min-width: 300px;
}

.toast-header {
  border-radius: 8px 8px 0 0;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>