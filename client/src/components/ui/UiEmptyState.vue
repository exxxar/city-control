<!-- client/src/components/ui/UiEmptyState.vue -->
<template>
  <div class="text-center py-5">
    <IconFa :name="icon" size="3.5rem" color="#adb5bd" />
    <h5 class="mt-3 text-dark fw-bold">{{ title }}</h5>
    <p class="text-muted">{{ description }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script>
import IconFa from './IconFa.vue'

export default {
  name: 'UiEmptyState',
  components: { IconFa },
  props: {
    icon: { type: String, default: 'bi-inbox' },
    title: { type: String, default: 'Нет данных' },
    description: { type: String, default: '' }
  }
}
</script>