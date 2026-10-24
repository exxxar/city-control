<!-- admin/src/components/users/UserEditModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Редактирование пользователя</h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="saveUser" class="modal-body">
        <div class="form-group">
          <label class="form-label">ФИО</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-user"></i>
            </span>
            <input
                v-model="form.full_name"
                type="text"
                class="form-control-custom"
                required
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Email</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-envelope"></i>
            </span>
            <input
                v-model="form.email"
                type="email"
                class="form-control-custom"
                required
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Телефон</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-phone"></i>
            </span>
            <input
                v-model="form.phone"
                type="tel"
                class="form-control-custom"
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Роль</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-user-tag"></i>
            </span>
            <select v-model="selectedRoleId" class="form-control-custom">
              <option v-for="role in roles" :key="role.id" :value="role.id">
                {{ role.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="$emit('close')">
            Отмена
          </button>
          <button type="submit" class="btn-save" :disabled="isSaving">
            <span v-if="isSaving" class="spinner-small"></span>
            <i v-else class="fas fa-check"></i>
            {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users.store'

const props = defineProps({
  user: { type: Object, required: true },
  roles: { type: Array, required: true }
})

const emit = defineEmits(['close', 'saved'])

const usersStore = useUsersStore()

const form = reactive({
  full_name: props.user.full_name,
  email: props.user.email,
  phone: props.user.phone
})

const selectedRoleId = ref(props.user.roles[0]?.id || 1)
const isSaving = ref(false)

async function saveUser() {
  isSaving.value = true
  try {
    // Обновляем роль, если она изменилась
    if (selectedRoleId.value !== props.user.roles[0]?.id) {
      await usersStore.changeRole(props.user.id, selectedRoleId.value)
    }

    // Здесь можно добавить вызов API для обновления других полей
    // await usersApi.update(props.user.id, form)

    emit('saved')
  } catch (error) {
    console.error('Save user error:', error)
  } finally {
    isSaving.value = false
  }
}
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.75rem;
  border-bottom: 1px solid #e8edf0;

  h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 800;
    color: #172f40;
  }
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #f1f5f9;
  color: #70808c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    background: #e2e8f0;
    color: #172f40;
  }
}

.modal-body {
  padding: 1.75rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.45rem;
  color: #172f40;
  font-size: 0.88rem;
  font-weight: 700;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #e8edf0;
  border-radius: 12px;
  background: #fcfcfd;
  transition: all 180ms ease;
  overflow: hidden;

  &:focus-within {
    border-color: #00a896;
    background: white;
    box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
  }
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  flex-shrink: 0;
  color: #70808c;
}

.form-control-custom {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.75rem 1rem 0.75rem 0;
  color: #172f40;
  font-size: 0.9rem;
  width: 100%;
  outline: none;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-save {
  flex: 1;
  padding: 0.85rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-cancel {
  background: #f1f5f9;
  border: 1px solid #e8edf0;
  color: #172f40;

  &:hover {
    background: #e2e8f0;
  }
}

.btn-save {
  background: linear-gradient(135deg, #00a896, #087e8b);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>