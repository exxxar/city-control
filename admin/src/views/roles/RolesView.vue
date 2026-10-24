<!-- admin/src/views/roles/RolesView.vue -->
<template>
  <div class="roles-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Роли и разрешения</h1>
        <p class="page-subtitle">Управление ролями пользователей и их правами доступа</p>
      </div>
      <button class="btn-primary" @click="openCreateModal">
        <i class="fas fa-plus"></i> Создать роль
      </button>
    </div>

    <Transition name="fade">
      <div v-if="rolesStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные.</span>
      </div>
    </Transition>

    <!-- Системные роли -->
    <div class="roles-section">
      <h2 class="section-title">
        <i class="fas fa-shield-halved"></i>
        Системные роли
        <span class="section-badge">Нельзя удалить</span>
      </h2>
      <div class="roles-grid">
        <div v-for="role in rolesStore.systemRoles" :key="role.id" class="role-card role-card--system">
          <div class="role-header">
            <div class="role-name">{{ role.name }}</div>
            <span class="system-badge">Системная</span>
          </div>
          <p class="role-desc">{{ role.description }}</p>
          <div class="role-stats">
            <span class="stat-item"><i class="fas fa-users"></i> {{ role.users_count }} польз.</span>
            <span class="stat-item"><i class="fas fa-key"></i> {{ role.permissions.length }} прав</span>
          </div>
          <div class="role-permissions-preview">
            <span v-for="p in role.permissions.slice(0, 4)" :key="p" class="perm-tag">{{ getPermLabel(p) }}</span>
            <span v-if="role.permissions.length > 4" class="perm-tag perm-tag--more">+{{ role.permissions.length - 4 }}</span>
          </div>
          <button class="btn-edit" @click="openEditModal(role)">
            <i class="fas fa-pen"></i> Редактировать разрешения
          </button>
        </div>
      </div>
    </div>

    <!-- Пользовательские роли -->
    <div class="roles-section">
      <h2 class="section-title">
        <i class="fas fa-user-tag"></i>
        Пользовательские роли
      </h2>
      <div v-if="rolesStore.customRoles.length === 0" class="empty-roles">
        <i class="fas fa-user-plus"></i>
        <p>Нет пользовательских ролей. Создайте первую!</p>
      </div>
      <div v-else class="roles-grid">
        <div v-for="role in rolesStore.customRoles" :key="role.id" class="role-card">
          <div class="role-header">
            <div class="role-name">{{ role.name }}</div>
            <div class="role-actions">
              <button class="icon-btn" @click="openEditModal(role)" title="Редактировать">
                <i class="fas fa-pen"></i>
              </button>
              <button class="icon-btn icon-btn--danger" @click="confirmDelete(role)" title="Удалить">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          <p class="role-desc">{{ role.description }}</p>
          <div class="role-stats">
            <span class="stat-item"><i class="fas fa-users"></i> {{ role.users_count }} польз.</span>
            <span class="stat-item"><i class="fas fa-key"></i> {{ role.permissions.length }} прав</span>
          </div>
          <div class="role-permissions-preview">
            <span v-for="p in role.permissions.slice(0, 4)" :key="p" class="perm-tag">{{ getPermLabel(p) }}</span>
            <span v-if="role.permissions.length > 4" class="perm-tag perm-tag--more">+{{ role.permissions.length - 4 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Матрица разрешений -->
    <div class="matrix-card">
      <h2 class="section-title">
        <i class="fas fa-table-cells"></i>
        Матрица разрешений
      </h2>
      <div class="matrix-wrapper">
        <table class="matrix-table">
          <thead>
          <tr>
            <th>Роль</th>
            <th v-for="group in permissionGroups" :key="group" :colspan="getGroupPerms(group).length" class="group-header">
              {{ group }}
            </th>
          </tr>
          <tr>
            <th></th>
            <th v-for="perm in ALL_PERMISSIONS" :key="perm.key" class="perm-header">
              <span :title="perm.label">{{ getPermShortLabel(perm.label) }}</span>
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="role in rolesStore.roles" :key="role.id">
            <td class="role-cell">{{ role.name }}</td>
            <td v-for="perm in ALL_PERMISSIONS" :key="perm.key" class="perm-cell">
                <span v-if="role.permissions.includes(perm.key)" class="perm-check">
                  <i class="fas fa-check"></i>
                </span>
              <span v-else class="perm-empty">—</span>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Модалка создания/редактирования роли -->
    <RoleEditModal
        v-if="editingRole"
        :role="editingRole"
        @close="editingRole = null"
        @saved="onRoleSaved"
    />

    <!-- Модалка подтверждения удаления -->
    <ConfirmModal
        v-if="confirmAction"
        :title="confirmAction.title"
        :message="confirmAction.message"
        confirm-text="Удалить"
        confirm-class="btn-danger"
        @confirm="confirmAction.callback()"
        @cancel="confirmAction = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRolesStore, ALL_PERMISSIONS } from '@/stores/roles.store'
import { useNotifications } from '@/composables/useNotifications'
import RoleEditModal from '@/components/roles/RoleEditModal.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'

const rolesStore = useRolesStore()
const { success, error: showError } = useNotifications()

const editingRole = ref(null)
const confirmAction = ref(null)

const permissionGroups = computed(() => {
  const groups = [...new Set(ALL_PERMISSIONS.map(p => p.group))]
  return groups
})

function getGroupPerms(group) {
  return ALL_PERMISSIONS.filter(p => p.group === group)
}

function getPermLabel(key) {
  const perm = ALL_PERMISSIONS.find(p => p.key === key)
  return perm ? perm.label : key
}

function getPermShortLabel(label) {
  // Сокращаем для заголовков таблицы
  const words = label.split(' ')
  return words.length > 2 ? words.slice(0, 2).join(' ') + '.' : label
}

function openCreateModal() {
  editingRole.value = {
    id: null,
    name: '',
    description: '',
    permissions: [],
    is_system: false
  }
}

function openEditModal(role) {
  editingRole.value = { ...role, permissions: [...role.permissions] }
}

async function onRoleSaved() {
  editingRole.value = null
  await rolesStore.fetchRoles()
  success('Роль успешно сохранена')
}

function confirmDelete(role) {
  confirmAction.value = {
    title: 'Удаление роли',
    message: `Вы уверены, что хотите удалить роль "${role.name}"? У ${role.users_count} пользователей эта роль будет сброшена до базовой.`,
    callback: async () => {
      try {
        await rolesStore.deleteRole(role.id)
        success('Роль удалена')
        confirmAction.value = null
      } catch (err) {
        showError('Ошибка при удалении роли')
      }
    }
  }
}

onMounted(() => {
  rolesStore.fetchRoles()
})
</script>

<style scoped lang="scss">
.roles-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

.btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #00a896, #087e8b); color: white; border: none; border-radius: 12px; font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.roles-section { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.75rem; }
.section-title { display: flex; align-items: center; gap: 0.75rem; margin: 0 0 1.5rem; font-size: 1.15rem; font-weight: 800; color: #172f40; }
.section-title i { color: #00a896; }
.section-badge { padding: 0.25rem 0.6rem; background: rgba(113, 128, 150, 0.12); color: #70808c; font-size: 0.72rem; font-weight: 700; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.05em; }

.roles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }

.role-card { background: #f8fafc; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; transition: all 0.2s ease; }
.role-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(23, 47, 64, 0.08); }
.role-card--system { background: linear-gradient(135deg, rgba(0, 168, 150, 0.03), rgba(0, 168, 150, 0.01)); border-color: rgba(0, 168, 150, 0.2); }

.role-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; gap: 0.5rem; }
.role-name { font-size: 1.1rem; font-weight: 800; color: #172f40; }
.role-actions { display: flex; gap: 0.5rem; }
.system-badge { padding: 0.25rem 0.6rem; background: rgba(0, 168, 150, 0.12); color: #00a896; font-size: 0.72rem; font-weight: 700; border-radius: 6px; white-space: nowrap; }

.role-desc { margin: 0 0 1rem; color: #70808c; font-size: 0.88rem; line-height: 1.5; }

.role-stats { display: flex; gap: 1rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #e8edf0; }
.stat-item { display: inline-flex; align-items: center; gap: 0.35rem; color: #172f40; font-size: 0.82rem; font-weight: 600; }
.stat-item i { color: #00a896; font-size: 0.85rem; }

.role-permissions-preview { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 1rem; }
.perm-tag { padding: 0.25rem 0.6rem; background: white; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.72rem; color: #172f40; font-weight: 600; }
.perm-tag--more { background: #00a896; color: white; border-color: #00a896; }

.btn-edit { width: 100%; padding: 0.65rem; background: white; border: 1px solid #e8edf0; border-radius: 10px; color: #172f40; font-size: 0.85rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transition: all 0.2s ease; }
.btn-edit:hover { background: #00a896; color: white; border-color: #00a896; }

.icon-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: white; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.icon-btn:hover { background: #e2e8f0; color: #172f40; }
.icon-btn--danger:hover { background: #fee2e2; color: #c64752; }

.empty-roles { text-align: center; padding: 3rem 1rem; color: #70808c; }
.empty-roles i { font-size: 2.5rem; opacity: 0.3; margin-bottom: 0.75rem; }

/* Матрица разрешений */
.matrix-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.75rem; }
.matrix-wrapper { overflow-x: auto; }
.matrix-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.matrix-table th, .matrix-table td { padding: 0.65rem 0.5rem; text-align: center; border-bottom: 1px solid #f1f5f9; }
.matrix-table thead th { background: #f8fafc; font-weight: 700; color: #70808c; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.72rem; }
.group-header { background: rgba(0, 168, 150, 0.08) !important; color: #00a896 !important; font-size: 0.78rem !important; }
.perm-header span { display: block; font-size: 0.68rem; font-weight: 600; color: #70808c; }
.role-cell { text-align: left !important; font-weight: 700; color: #172f40; white-space: nowrap; padding-left: 1rem !important; }
.perm-check { color: #06d6a0; font-size: 1rem; }
.perm-empty { color: #cbd5e1; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 767.98px) {
  .roles-grid { grid-template-columns: 1fr; }
}
</style>