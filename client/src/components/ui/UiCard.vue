<!-- client/src/components/ui/UiCard.vue -->
<template>
  <div :class="['card', cardClasses]" :style="cardStyle">
    <div v-if="$slots.header || title" class="card-header" :class="headerClasses">
      <slot name="header">
        <h5 v-if="title" class="card-title mb-0">{{ title }}</h5>
      </slot>
    </div>

    <div class="card-body" :class="bodyClasses">
      <slot></slot>
    </div>

    <div v-if="$slots.footer" class="card-footer" :class="footerClasses">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UiCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    noPadding: {
      type: Boolean,
      default: false
    },
    hoverable: {
      type: Boolean,
      default: false
    },
    clickable: {
      type: Boolean,
      default: false
    },
    shadow: {
      type: String,
      default: 'sm',
      validator: (v) => ['', 'sm', 'lg'].includes(v)
    },
    background: {
      type: String,
      default: ''
    }
  },
  computed: {
    cardClasses() {
      return [
        this.hoverable ? 'card-hoverable' : '',
        this.clickable ? 'card-clickable' : '',
        this.shadow ? `shadow-${this.shadow}` : ''
      ].filter(Boolean)
    },
    headerClasses() {
      return ['bg-white', 'border-bottom']
    },
    bodyClasses() {
      return [
        this.noPadding ? 'p-0' : ''
      ].filter(Boolean)
    },
    footerClasses() {
      return ['bg-white', 'border-top']
    },
    cardStyle() {
      return this.background ? { backgroundColor: this.background } : {}
    }
  }
}
</script>

<style scoped>
.card {
  border: 1px solid #e9ecef;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.card-hoverable:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-clickable {
  cursor: pointer;
}

.card-clickable:hover {
  border-color: var(--civic-primary, #00A896);
}

.card-header {
  border-radius: 12px 12px 0 0 !important;
  padding: 1rem 1.25rem;
}

.card-footer {
  border-radius: 0 0 12px 12px !important;
  padding: 1rem 1.25rem;
}

.card-title {
  font-weight: 600;
  color: #212529;
}
</style>