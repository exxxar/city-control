<!-- client/src/components/ui/UiBottomSheet.vue -->
<template>
  <Teleport to="body">
    <Transition name="bottom-sheet">
      <div
        v-if="modelValue"
        class="bottom-sheet-overlay"
        @click.self="closeOnBackdrop && close()"
      >
        <div :class="['bottom-sheet', heightClass]">
          <div class="bottom-sheet-handle" @click="close">
            <div class="handle-bar"></div>
          </div>

          <div v-if="$slots.header || title" class="bottom-sheet-header">
            <slot name="header">
              <h5 class="bottom-sheet-title">{{ title }}</h5>
            </slot>
            <button
              v-if="closable"
              type="button"
              class="btn-close"
              @click="close"
            ></button>
          </div>

          <div class="bottom-sheet-body">
            <slot></slot>
          </div>

          <div v-if="$slots.footer" class="bottom-sheet-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: 'UiBottomSheet',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: 'auto',
      validator: (v) => ['auto', 'small', 'medium', 'large', 'full'].includes(v)
    },
    closable: {
      type: Boolean,
      default: true
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue', 'close'],
  computed: {
    heightClass() {
      return `bottom-sheet-${this.height}`
    }
  },
  watch: {
    modelValue(val) {
      if (val) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    }
  },
  beforeUnmount() {
    document.body.style.overflow = ''
  },
  methods: {
    close() {
      this.$emit('update:modelValue', false)
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.bottom-sheet-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1050;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bottom-sheet {
  background-color: white;
  border-radius: 16px 16px 0 0;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
}

.bottom-sheet-auto {
  height: auto;
}

.bottom-sheet-small {
  height: 40vh;
}

.bottom-sheet-medium {
  height: 60vh;
}

.bottom-sheet-large {
  height: 80vh;
}

.bottom-sheet-full {
  height: 90vh;
}

.bottom-sheet-handle {
  padding: 12px;
  display: flex;
  justify-content: center;
  cursor: pointer;
}

.handle-bar {
  width: 40px;
  height: 4px;
  background-color: #dee2e6;
  border-radius: 2px;
}

.bottom-sheet-header {
  padding: 0 1.5rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e9ecef;
}

.bottom-sheet-title {
  font-weight: 600;
  color: #212529;
  margin: 0;
}

.bottom-sheet-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.bottom-sheet-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

/* Animations */
.bottom-sheet-enter-active,
.bottom-sheet-leave-active {
  transition: all 0.3s ease;
}

.bottom-sheet-enter-from,
.bottom-sheet-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>