<!-- admin/src/components/users/AssignRoleModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card modal-card--small">
      <div class="modal-header">
        <h2>Назначение роли</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <div class="modal-body">
        <div class="user-info-block">
          <div class="user-avatar">{{ getInitials(user.full_name) }}</div>
          <div class="user-details">
            <div class="user-name">{{ user.full_name }}</div>
            <div class="user-email">{{ user.email }}</div>
            <div class="user-current-role">
              Текущая роль: <strong>{{ user.roles[0]?.name || 'Не назначена' }}</strong>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Новая роль</label>
          <div class="roles-list">
            <label
                v-for="role in roles"
                :key="role.id"
                class="role-option"
                :class="{ selected: selectedRoleId === role.id }"
            >
              <input type="radio" :value="role.id" v-model="selectedRoleId" class="role-radio">
              <div class="role-option-content">
                <div class="role-option-name">{{ role.name }}</div>
                <div class="role-option-desc">{{ role.description }}</div>
              </div>
              <span v-if="role.is_system" class="system-mark">системная</span>
            </label>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="$emit('close')">Отмена</button>
          <button type="button" class="btn-save" @click="handleAssign" :disabled="isSaving || !selectedRoleId">
            <span v-if="isSaving" class="spinner-small"></span>
            <i v-else class="fas fa-check"></i>
            {{ isSaving ? 'Сохранение...' : 'Назначить роль' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users.store'
import { useRolesStore } from '@/stores/roles.store'

const props = defineProps({
  user: { type: Object, required: true }
})

const emit = defineEmits(['close', 'assigned'])

const usersStore = useUsersStore()
const rolesStore = useRolesStore()

const selectedRoleId = ref(props.user.roles[0]?.id || null)
const isSaving = ref(false)

function getInitials(fullName) {
  if (!fullName) return '?'
  return fullName.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

async function handleAssign() {
  if (!selectedRoleId.value) return

  isSaving.value = true
  try {
    await usersStore.changeRole(props.user.id, selectedRoleId.value)
    emit('assigned')
  } catch (error) {
    console.error('Assign role error:', error)
  } finally {
    isSaving.value = false
  }
}

onMounted(async () => {
  if (rolesStore.roles.length === 0) {
    await rolesStore.fetchRoles()
  }
})
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }
.modal-card--small { max-width: 500px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; }

.user-info-block { display: flex; gap: 1rem; padding: 1rem; background: #f8fafc; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #e8edf0; }
.user-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #00a896, #087e8b); color: white; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 700; flex-shrink: 0; }
.user-details { flex: 1; min-width: 0; }
.user-name { font-weight: 700; color: #172f40; font-size: 0.95rem; margin-bottom: 0.15rem; }
.user-email { color: #70808c; font-size: 0.82rem; margin-bottom: 0.35rem; }
.user-current-role { font-size: 0.82rem; color: #70808c; }
.user-current-role strong { color: #00a896; }

.form-group { margin-bottom: 1.5rem; }
.form-label { display: block; margin-bottom: 0.75rem; color: #172f40; font-size: 0.88rem; font-weight: 700; }

.roles-list { display: flex; flex-direction: column; gap: 0.5rem; max-height: 300px; overflow-y: auto; }
.role-option { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.85rem 1rem; background: #f8fafc; border: 2px solid #e8edf0; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; }
.role-option:hover { border-color: #00a896; background: rgba(0, 168, 150, 0.03); }
.role-option.selected { border-color: #00a896; background: rgba(0, 168, 150, 0.08); }

.role-radio { display: none; }
.role-option-content { flex: 1; min-width: 0; }
.role-option::before { content: ''; width: 20px; height: 20px; border: 2px solid #cbd5e1; border-radius: 50%; flex-shrink: 0; margin-top: 2px; transition: all 0.2s ease; }
.role-option.selected::before { border-color: #00a896; background: #00a896; box-shadow: inset 0 0 0 3px white; }

.role-option-name { font-weight: 700; color: #172f40; font-size: 0.9rem; margin-bottom: 0.15rem; display: flex; align-items: center; gap: 0.5rem; }
.role-option-desc { color: #70808c; font-size: 0.78rem; line-height: 1.4; }

.system-mark { padding: 0.1rem 0.4rem; background: rgba(113, 128, 150, 0.12); color: #70808c; font-size: 0.65rem; font-weight: 700; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em; }

.modal-footer { display: flex; gap: 0.75rem; }
.btn-cancel, .btn-save { flex: 1; padding: 0.85rem; border-radius: 12px; font-size: 0.95rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; justify-content: center; gap: 0.5rem; border: none; }
.btn-cancel { background: #f1f5f9; color: #172f40; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-save { background: linear-gradient(135deg, #00a896, #087e8b); color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-save:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner-small { width: 16px; height: 16px; border: 2px solid rgba(255, 255, 255, 0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>