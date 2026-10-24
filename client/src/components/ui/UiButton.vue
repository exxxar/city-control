<!-- client/src/components/ui/UiButton.vue -->
<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status">
      <span class="visually-hidden">Загрузка...</span>
    </span>
    <i v-if="icon && !loading" :class="icon" class="me-2"></i>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'UiButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (v) => ['primary', 'secondary', 'success', 'danger', 'warning', 'outline-primary', 'outline-secondary', 'link'].includes(v)
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    },
    type: {
      type: String,
      default: 'button'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    block: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    }
  },
  emits: ['click'],
  computed: {
    buttonClasses() {
      return [
        'btn',
        `btn-${this.variant}`,
        this.size !== 'md' ? `btn-${this.size}` : '',
        this.block ? 'w-100' : ''
      ].filter(Boolean)
    }
  }
}
</script>

<style scoped>
.btn {
  transition: all 0.2s ease;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.btn-primary {
  background-color: var(--civic-primary, #00A896);
  border-color: var(--civic-primary, #00A896);
}

.btn-primary:hover:not(:disabled) {
  background-color: #008f80;
  border-color: #008f80;
}

.btn-outline-primary {
  color: var(--civic-primary, #00A896);
  border-color: var(--civic-primary, #00A896);
}

.btn-outline-primary:hover:not(:disabled) {
  background-color: var(--civic-primary, #00A896);
  color: white;
}
</style>