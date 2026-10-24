<!-- client/src/components/ui/UiModal.vue -->
<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="modal fade show d-block"
      tabindex="-1"
      @click.self="closeOnBackdrop && close()"
    >
      <div :class="['modal-dialog', sizeClass, 'modal-dialog-centered']">
        <div class="modal-content border-0 shadow">
          <div v-if="$slots.header || title" class="modal-header">
            <slot name="header">
              <h5 class="modal-title">{{ title }}</h5>
            </slot>
            <button
              v-if="closable"
              type="button"
              class="btn-close"
              @click="close"
            ></button>
          </div>

          <div class="modal-body">
            <slot></slot>
          </div>

          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>

    <div v-if="modelValue" class="modal-backdrop fade show"></div>
  </Teleport>
</template>

<script>
export default {
  name: 'UiModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v)
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
    sizeClass() {
      return this.size !== 'md' ? `modal-${this.size}` : ''
    }
  },
  watch: {
    modelValue(val) {
      if (val) {
        document.body.classList.add('modal-open')
        document.body.style.overflow = 'hidden'
      } else {
        document.body.classList.remove('modal-open')
        document.body.style.overflow = ''
      }
    }
  },
  beforeUnmount() {
    document.body.classList.remove('modal-open')
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
.modal-content {
  border-radius: 12px;
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  padding: 1.25rem 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  border-top: 1px solid #e9ecef;
  padding: 1rem 1.5rem;
}

.modal-title {
  font-weight: 600;
  color: #212529;
}
</style>