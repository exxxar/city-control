<!-- client/src/components/layout/AppPageContainer.vue -->
<template>
  <div class="app-page-container container py-3 pb-5 pb-md-3">
    <div v-if="title || $slots.header" class="page-header mb-3">
      <slot name="header">
        <div class="d-flex align-items-center justify-content-between">
          <h4 class="mb-0 fw-bold text-dark">{{ title }}</h4>
          <slot name="actions"></slot>
        </div>
        <p v-if="subtitle" class="text-muted small mt-1 mb-0">{{ subtitle }}</p>
      </slot>
    </div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'AppPageContainer',
  props: {
    title: { type: String, default: '' },
    subtitle: { type: String, default: '' }
  }
}
</script>