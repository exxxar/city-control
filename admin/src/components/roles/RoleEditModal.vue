<!-- admin/src/components/roles/RoleEditModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>{{ isEdit ? 'Редактирование роли' : 'Создание роли' }}</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <form @submit.prevent="saveRole" class="modal-body">
        <div class="form-group">
          <label class="form-label">Название роли *</label>
          <div class="input-wrapper">
            <span class="input-icon"><i class="fas fa-user-tag"></i></span>
            <input v-model="form.name" type="text" class="form-control-custom" placeholder="Например: Аудитор" required :disabled="form.is_system">
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Описание</label>
          <textarea v-model="form.description" rows="2" class="form-control-custom textarea" placeholder="Краткое описание назначения роли"></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Разрешения</label>
          <p class="form-hint">Отметьте права, которые будут у этой роли</p>

          <div class="permissions-matrix">
            <div v-for="group in permissionGroups" :key="group" class="perm-group">
              <div class="perm-group-header">
                <span class="perm-group-title">{{ group }}</span>
                <button type="button" class="select-all-btn" @click="toggleGroup(group)">
                  {{ isGroupSelected(group) ? 'Снять все' : 'Выбрать все' }}
                </button>
              </div>
              <div class="perm-list">
                <label v-for="perm in getGroupPerms(group)" :key="perm.key" class="perm-item">
                  <input type="checkbox" :value="perm.key" v-model="form.permissions" class="perm-checkbox">
                  <span class="perm-checkmark"></span>
                  <span class="perm-label">{{ perm.label }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="selected-count">
          Выбрано разрешений: <strong>{{ form.permissions.length }}</strong> из {{ ALL_PERMISSIONS.length }}
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="$emit('close')">Отмена</button>
          <button type="submit" class="btn-save" :disabled="isSaving || !form.name.trim()">
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
import { ref, reactive, computed } from 'vue'
import { useRolesStore, ALL_PERMISSIONS } from '@/stores/roles.store'

const props = defineProps({
  role: { type: Object, required: true }
})

const emit = defineEmits(['close', 'saved'])

const rolesStore = useRolesStore()
const isSaving = ref(false)

const isEdit = computed(() => props.role.id !== null)

const form = reactive({
  name: props.role.name || '',
  description: props.role.description || '',
  permissions: [...(props.role.permissions || [])],
  is_system: props.role.is_system || false
})

const permissionGroups = computed(() => {
  return [...new Set(ALL_PERMISSIONS.map(p => p.group))]
})

function getGroupPerms(group) {
  return ALL_PERMISSIONS.filter(p => p.group === group)
}

function isGroupSelected(group) {
  const groupPerms = getGroupPerms(group)
  return groupPerms.every(p => form.permissions.includes(p.key))
}

function toggleGroup(group) {
  const groupPerms = getGroupPerms(group).map(p => p.key)
  if (isGroupSelected(group)) {
    form.permissions = form.permissions.filter(p => !groupPerms.includes(p))
  } else {
    const newPerms = [...new Set([...form.permissions, ...groupPerms])]
    form.permissions = newPerms
  }
}

async function saveRole() {
  if (!form.name.trim()) return

  isSaving.value = true
  try {
    const payload = {
      name: form.name,
      description: form.description,
      permissions: form.permissions
    }

    if (isEdit.value) {
      await rolesStore.updateRole(props.role.id, payload)
    } else {
      await rolesStore.createRole(payload)
    }
    emit('saved')
  } catch (error) {
    console.error('Save role error:', error)
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 650px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; position: sticky; top: 0; background: white; z-index: 1; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; }
.form-group { margin-bottom: 1.5rem; }
.form-label { display: block; margin-bottom: 0.45rem; color: #172f40; font-size: 0.88rem; font-weight: 700; }
.form-hint { margin: 0 0 1rem; color: #70808c; font-size: 0.82rem; }

.input-wrapper { display: flex; align-items: center; border: 1px solid #e8edf0; border-radius: 12px; background: #fcfcfd; transition: all 180ms ease; overflow: hidden; }
.input-wrapper:focus-within { border-color: #00a896; background: white; box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1); }
.input-icon { display: flex; align-items: center; justify-content: center; width: 42px; flex-shrink: 0; color: #70808c; }
.form-control-custom { flex: 1; border: none; background: transparent; padding: 0.75rem 1rem 0.75rem 0; color: #172f40; font-size: 0.9rem; width: 100%; outline: none; }
.form-control-custom.textarea { resize: vertical; min-height: 60px; font-family: inherit; padding: 0.75rem 1rem; }
.form-control-custom:disabled { background: #f1f5f9; cursor: not-allowed; }

.permissions-matrix { display: flex; flex-direction: column; gap: 1rem; }
.perm-group { background: #f8fafc; border: 1px solid #e8edf0; border-radius: 12px; padding: 1rem; }
.perm-group-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.perm-group-title { font-weight: 700; color: #172f40; font-size: 0.9rem; }
.select-all-btn { background: none; border: none; color: #00a896; font-size: 0.78rem; font-weight: 600; cursor: pointer; padding: 0.25rem 0.5rem; border-radius: 6px; transition: background 0.2s ease; }
.select-all-btn:hover { background: rgba(0, 168, 150, 0.1); }

.perm-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem; }
.perm-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: white; border: 1px solid #e8edf0; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; font-size: 0.85rem; }
.perm-item:hover { border-color: #00a896; background: rgba(0, 168, 150, 0.03); }
.perm-item:has(.perm-checkbox:checked) { background: rgba(0, 168, 150, 0.08); border-color: #00a896; }

.perm-checkbox { display: none; }
.perm-checkmark { width: 18px; height: 18px; border: 2px solid #cbd5e1; border-radius: 4px; flex-shrink: 0; position: relative; transition: all 0.2s ease; }
.perm-checkbox:checked + .perm-checkmark { background: #00a896; border-color: #00a896; }
.perm-checkbox:checked + .perm-checkmark::after { content: ''; position: absolute; left: 4px; top: 1px; width: 5px; height: 9px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); }
.perm-label { color: #172f40; font-weight: 500; }

.selected-count { margin-top: 1rem; padding: 0.75rem 1rem; background: #f8fafc; border-radius: 10px; color: #70808c; font-size: 0.88rem; text-align: center; }
.selected-count strong { color: #00a896; font-size: 1rem; }

.modal-footer { display: flex; gap: 0.75rem; margin-top: 1.5rem; }
.btn-cancel, .btn-save { flex: 1; padding: 0.85rem; border-radius: 12px; font-size: 0.95rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.btn-cancel { background: #f1f5f9; border: 1px solid #e8edf0; color: #172f40; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-save { background: linear-gradient(135deg, #00a896, #087e8b); border: none; color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-save:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }
.spinner-small { width: 16px; height: 16px; border: 2px solid rgba(255, 255, 255, 0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>