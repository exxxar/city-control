<!-- client/src/components/ui/UiSkeleton.vue -->
<template>
  <div :class="['skeleton', typeClass, animated ? 'skeleton-animated' : '']" :style="style"></div>
</template>

<script>
export default {
  name: 'UiSkeleton',
  props: {
    type: {
      type: String,
      default: 'text',
      validator: (v) => ['text', 'circle', 'rect', 'card'].includes(v)
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '1rem'
    },
    animated: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    typeClass() {
      return `skeleton-${this.type}`
    },
    style() {
      return {
        width: this.width,
        height: this.height
      }
    }
  }
}
</script>

<style scoped>
.skeleton {
  background-color: #e9ecef;
  border-radius: 4px;
}

.skeleton-circle {
  border-radius: 50%;
}

.skeleton-card {
  border-radius: 12px;
}

.skeleton-animated {
  background: linear-gradient(90deg, #e9ecef 25%, #f8f9fa 50%, #e9ecef 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>