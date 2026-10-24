<!-- client/src/components/ui/UiBadge.vue -->
<template>
  <span :class="badgeClasses">
    <i v-if="icon" :class="icon" class="me-1"></i>
    <slot></slot>
  </span>
</template>

<script>
export default {
  name: 'UiBadge',
  props: {
    variant: {
      type: String,
      default: 'secondary',
      validator: (v) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'].includes(v)
    },
    pill: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    }
  },
  computed: {
    badgeClasses() {
      return [
        'badge',
        `bg-${this.variant}`,
        this.pill ? 'rounded-pill' : '',
        this.size !== 'md' ? `badge-${this.size}` : ''
      ].filter(Boolean)
    }
  }
}
</script>

<style scoped>
.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
}

.badge-sm {
  font-size: 0.75em;
  padding: 0.25em 0.5em;
}

.badge-lg {
  font-size: 1em;
  padding: 0.5em 0.75em;
}

.bg-primary {
  background-color: var(--civic-primary, #00A896) !important;
}

.bg-success {
  background-color: #06D6A0 !important;
}

.bg-warning {
  background-color: #FFD166 !important;
  color: #212529 !important;
}

.bg-danger {
  background-color: #EF476F !important;
}
</style>