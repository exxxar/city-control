<!-- admin/src/components/ui/ConfirmModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>{{ title }}</h2>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" @click="$emit('cancel')">
          Отмена
        </button>
        <button :class="['btn-confirm', confirmClass]" @click="$emit('confirm')">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  message: { type: String, required: true },
  confirmText: { type: String, default: 'Подтвердить' },
  confirmClass: { type: String, default: 'btn-primary' }
})

defineEmits(['confirm', 'cancel'])
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(23, 47, 64, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-card {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid #e8edf0;

  h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
    color: #172f40;
  }
}

.modal-body {
  padding: 1.5rem 1.75rem;

  p {
    margin: 0;
    color: #172f40;
    font-size: 0.95rem;
    line-height: 1.6;
  }
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem 1.75rem;
  border-top: 1px solid #e8edf0;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 0.85rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel {
  background: #f1f5f9;
  border: 1px solid #e8edf0;
  color: #172f40;

  &:hover {
    background: #e2e8f0;
  }
}

.btn-confirm {
  border: none;
  color: white;

  &.btn-primary {
    background: linear-gradient(135deg, #00a896, #087e8b);
    box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
    }
  }

  &.btn-danger {
    background: linear-gradient(135deg, #c64752, #a83a44);
    box-shadow: 0 4px 12px rgba(198, 71, 82, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(198, 71, 82, 0.35);
    }
  }

  &.btn-success {
    background: linear-gradient(135deg, #06d6a0, #05b88a);
    box-shadow: 0 4px 12px rgba(6, 214, 160, 0.25);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(6, 214, 160, 0.35);
    }
  }
}
</style>