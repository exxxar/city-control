<!-- admin/src/views/users/UsersView.vue -->
<template>
  <div class="users-page">
    <!-- Заголовок -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Пользователи</h1>
        <p class="page-subtitle">Управление аккаунтами и доступами</p>
        <button class="btn-export" @click="handleExport">
          <i class="fas fa-file-excel"></i>
          Экспорт в Excel
        </button>
      </div>
      <div class="page-stats">
        <div class="stat-badge stat-badge--success">
          <i class="fas fa-user-check"></i>
          <span>{{ usersStore.activeUsersCount }} активных</span>
        </div>
        <div class="stat-badge stat-badge--danger">
          <i class="fas fa-user-slash"></i>
          <span>{{ usersStore.blockedUsersCount }} заблокированных</span>
        </div>
      </div>
    </div>



    <!-- Уведомление о моковых данных -->
    <Transition name="fade">
      <div v-if="usersStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные. API пользователей на бэкенде пока не настроен.</span>
      </div>
    </Transition>

    <!-- Фильтры -->
    <div class="filters-card">
      <div class="filters-grid">
        <!-- Поиск -->
        <div class="filter-group">
          <label class="filter-label">Поиск</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-search"></i>
            </span>
            <input
                v-model="filters.search"
                type="text"
                class="form-control-custom"
                placeholder="Имя, email или телефон"
                @input="debouncedSearch"
            >
          </div>
        </div>

        <!-- Роль -->
        <div class="filter-group">
          <label class="filter-label">Роль</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-user-tag"></i>
            </span>
            <select v-model="filters.role" class="form-control-custom" @change="applyFilters">
              <option value="">Все роли</option>
              <option v-for="role in usersStore.roles" :key="role.id" :value="role.id">
                {{ role.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Статус -->
        <div class="filter-group">
          <label class="filter-label">Статус</label>
          <div class="input-wrapper">
            <span class="input-icon">
              <i class="fas fa-circle-check"></i>
            </span>
            <select v-model="filters.status" class="form-control-custom" @change="applyFilters">
              <option value="">Все статусы</option>
              <option value="active">Активные</option>
              <option value="blocked">Заблокированные</option>
            </select>
          </div>
        </div>

        <!-- Кнопка сброса -->
        <div class="filter-group">
          <label class="filter-label">&nbsp;</label>
          <button class="btn-reset" @click="resetFilters">
            <i class="fas fa-rotate-left"></i>
            Сбросить
          </button>
        </div>
      </div>
    </div>

    <!-- Таблица пользователей -->
    <div class="table-card">
      <div v-if="usersStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка пользователей...</p>
      </div>

      <div v-else-if="usersStore.users.length === 0" class="empty-state">
        <i class="fas fa-users-slash"></i>
        <h3>Пользователи не найдены</h3>
        <p>Попробуйте изменить параметры поиска</p>
      </div>

      <div v-else class="table-wrapper">
        <table class="users-table">
          <thead>
          <tr>
            <th>Пользователь</th>
            <th>Контакты</th>
            <th>Роль</th>
            <th>Статус</th>
            <th>Последний вход</th>
            <th class="actions-column">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="user in usersStore.users" :key="user.id">
            <!-- Пользователь -->
            <td>
              <div class="user-cell">
                <div class="user-avatar">
                  {{ getInitials(user.full_name) }}
                </div>
                <div class="user-info">
                  <div class="user-name">{{ user.full_name }}</div>
                  <div class="user-id">ID: {{ user.id }}</div>
                </div>
              </div>
            </td>

            <!-- Контакты -->
            <td>
              <div class="contacts-cell">
                <div class="contact-item">
                  <i class="fas fa-envelope"></i>
                  <span>{{ user.email }}</span>
                </div>
                <div class="contact-item">
                  <i class="fas fa-phone"></i>
                  <span>{{ user.phone }}</span>
                </div>
              </div>
            </td>

            <!-- Роль -->
            <!-- В таблице замените ячейку роли -->
            <td>
              <button class="role-badge-btn" :class="getRoleClass(user.roles[0]?.name)" @click="openAssignRoleModal(user)" title="Нажмите, чтобы изменить роль">
                {{ user.roles[0]?.name || 'Не назначена' }}
                <i class="fas fa-chevron-down"></i>
              </button>
            </td>


            <!-- Статус -->
            <td>
                <span class="status-badge" :class="user.is_active ? 'status-active' : 'status-blocked'">
                  <span class="status-dot"></span>
                  {{ user.is_active ? 'Активен' : 'Заблокирован' }}
                </span>
            </td>

            <!-- Последний вход -->
            <td>
              <div class="date-cell">
                {{ formatDate(user.last_login) }}
              </div>
            </td>

            <!-- Действия -->
            <td>
              <div class="actions-cell">
                <button
                    class="action-btn action-btn--edit"
                    @click="openEditModal(user)"
                    title="Редактировать"
                >
                  <i class="fas fa-pen"></i>
                </button>
                <button
                    v-if="user.is_active"
                    class="action-btn action-btn--block"
                    @click="confirmBlock(user)"
                    title="Заблокировать"
                >
                  <i class="fas fa-ban"></i>
                </button>
                <button
                    v-else
                    class="action-btn action-btn--unblock"
                    @click="confirmUnblock(user)"
                    title="Разблокировать"
                >
                  <i class="fas fa-unlock"></i>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Пагинация -->
      <div v-if="usersStore.pagination.pages > 1" class="pagination">
        <button
            class="pagination-btn"
            :disabled="usersStore.pagination.page === 1"
            @click="goToPage(usersStore.pagination.page - 1)"
        >
          <i class="fas fa-chevron-left"></i>
        </button>

        <span class="pagination-info">
          Страница {{ usersStore.pagination.page }} из {{ usersStore.pagination.pages }}
        </span>

        <button
            class="pagination-btn"
            :disabled="usersStore.pagination.page === usersStore.pagination.pages"
            @click="goToPage(usersStore.pagination.page + 1)"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <UserEditModal
        v-if="editingUser"
        :user="editingUser"
        :roles="usersStore.roles"
        @close="editingUser = null"
        @saved="onUserSaved"
    />

    <!-- Модальное окно подтверждения -->
    <ConfirmModal
        v-if="confirmAction"
        :title="confirmAction.title"
        :message="confirmAction.message"
        :confirm-text="confirmAction.confirmText"
        :confirm-class="confirmAction.confirmClass"
        @confirm="confirmAction.callback()"
        @cancel="confirmAction = null"
    />

    <!-- В конце шаблона, рядом с другими модалками -->
    <AssignRoleModal
        v-if="assigningUser"
        :user="assigningUser"
        @close="assigningUser = null"
        @assigned="onRoleAssigned"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users.store'
import { useNotifications } from '@/composables/useNotifications'
import UserEditModal from '@/components/users/UserEditModal.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import { useExport } from '@/composables/useExport'
import AssignRoleModal from '@/components/users/AssignRoleModal.vue'
import { useRolesStore } from '@/stores/roles.store'
const { exportToExcel } = useExport()

function handleExport() {
  exportToExcel(
      usersStore.users,
      'пользователи',
      'Пользователи',
      {
        id: 'ID',
        full_name: 'ФИО',
        email: 'Email',
        phone: 'Телефон',
        'roles.0.name': 'Роль',
        is_active: 'Статус',
        created_at: 'Дата регистрации'
      }
  )
}
const usersStore = useUsersStore()
const { success, error: showError } = useNotifications()

const filters = reactive({
  search: '',
  role: '',
  status: ''
})

const rolesStore = useRolesStore()
const assigningUser = ref(null)

function openAssignRoleModal(user) {
  assigningUser.value = { ...user }
}

async function onRoleAssigned() {
  assigningUser.value = null
  await loadUsers()
  success('Роль пользователя изменена')
}

const editingUser = ref(null)
const confirmAction = ref(null)

let searchTimeout = null

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 300)
}

function applyFilters() {
  usersStore.pagination.page = 1
  loadUsers()
}

function resetFilters() {
  filters.search = ''
  filters.role = ''
  filters.status = ''
  applyFilters()
}

function goToPage(page) {
  usersStore.pagination.page = page
  loadUsers()
}

async function loadUsers() {
  const params = {
    page: usersStore.pagination.page,
    per_page: usersStore.pagination.per_page
  }

  if (filters.search) params.search = filters.search
  if (filters.role) params.role = filters.role
  if (filters.status) params.status = filters.status

  await usersStore.fetchUsers(params)
}

function getInitials(fullName) {
  if (!fullName) return '?'
  const parts = fullName.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return fullName[0].toUpperCase()
}

function getRoleClass(roleName) {
  const classes = {
    'Системный администратор': 'role-admin',
    'Руководитель органа': 'role-manager',
    'Модератор': 'role-moderator',
    'Исполнитель': 'role-executor',
    'Пользователь': 'role-user'
  }
  return classes[roleName] || 'role-user'
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function openEditModal(user) {
  editingUser.value = { ...user }
}

async function onUserSaved() {
  editingUser.value = null
  await loadUsers()
  success('Пользователь успешно обновлён')
}

function confirmBlock(user) {
  confirmAction.value = {
    title: 'Заблокировать пользователя',
    message: `Вы уверены, что хотите заблокировать пользователя "${user.full_name}"? Он не сможет войти в систему.`,
    confirmText: 'Заблокировать',
    confirmClass: 'btn-danger',
    callback: async () => {
      try {
        await usersStore.blockUser(user.id)
        success('Пользователь заблокирован')
        confirmAction.value = null
      } catch (err) {
        showError('Ошибка блокировки пользователя')
      }
    }
  }
}

function confirmUnblock(user) {
  confirmAction.value = {
    title: 'Разблокировать пользователя',
    message: `Вы уверены, что хотите разблокировать пользователя "${user.full_name}"?`,
    confirmText: 'Разблокировать',
    confirmClass: 'btn-success',
    callback: async () => {
      try {
        await usersStore.unblockUser(user.id)
        success('Пользователь разблокирован')
        confirmAction.value = null
      } catch (err) {
        showError('Ошибка разблокировки пользователя')
      }
    }
  }
}

onMounted(async () => {
  await rolesStore.fetchRoles()
  await usersStore.fetchRoles()
  await loadUsers()
})
</script>

<style scoped lang="scss">
.users-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
}

.page-subtitle {
  margin: 0.25rem 0 0;
  color: #70808c;
  font-size: 0.95rem;
}

.page-stats {
  display: flex;
  gap: 0.75rem;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;

  &--success {
    background: rgba(6, 214, 160, 0.12);
    color: #06d6a0;
  }

  &--danger {
    background: rgba(198, 71, 82, 0.12);
    color: #c64752;
  }
}

.mock-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1.25rem;
  background: #fff7df;
  border: 1px solid rgba(166, 108, 0, 0.2);
  border-radius: 12px;
  color: #a66c00;
  font-size: 0.88rem;
  font-weight: 600;
}

/* === Фильтры === */
.filters-card {
  background: white;
  border: 1px solid #e8edf0;
  border-radius: 16px;
  padding: 1.5rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-label {
  display: block;
  margin-bottom: 0.45rem;
  color: #172f40;
  font-size: 0.82rem;
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

  &::placeholder {
    color: #aab5bc;
  }
}

.btn-reset {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #f1f5f9;
  border: 1px solid #e8edf0;
  border-radius: 12px;
  color: #172f40;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #e2e8f0;
  }
}

/* === Таблица === */
.table-card {
  background: white;
  border: 1px solid #e8edf0;
  border-radius: 16px;
  overflow: hidden;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #70808c;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8edf0;
  border-top-color: #00a896;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  i {
    font-size: 3rem;
    opacity: 0.3;
    margin-bottom: 1rem;
  }

  h3 {
    margin: 0 0 0.5rem;
    font-size: 1.15rem;
    font-weight: 700;
    color: #172f40;
  }

  p {
    margin: 0;
    font-size: 0.9rem;
  }
}

.table-wrapper {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;

  th, td {
    padding: 1rem 1.25rem;
    text-align: left;
    border-bottom: 1px solid #f1f5f9;
  }

  th {
    background: #f8fafc;
    font-size: 0.78rem;
    font-weight: 700;
    color: #70808c;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  tbody tr {
    transition: background 0.15s ease;

    &:hover {
      background: #f8fafc;
    }

    &:last-child td {
      border-bottom: none;
    }
  }
}

.actions-column {
  width: 120px;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}

.user-name {
  font-weight: 700;
  color: #172f40;
  font-size: 0.92rem;
}

.user-id {
  color: #70808c;
  font-size: 0.75rem;
  margin-top: 0.15rem;
}

.contacts-cell {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #172f40;
  font-size: 0.85rem;

  i {
    color: #70808c;
    font-size: 0.75rem;
    width: 14px;
  }
}

.role-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;

  &.role-admin {
    background: rgba(111, 66, 193, 0.12);
    color: #6f42c1;
  }

  &.role-manager {
    background: rgba(13, 202, 240, 0.12);
    color: #0dcaf0;
  }

  &.role-moderator {
    background: rgba(253, 126, 20, 0.12);
    color: #fd7e14;
  }

  &.role-executor {
    background: rgba(0, 168, 150, 0.12);
    color: #00a896;
  }

  &.role-user {
    background: rgba(113, 128, 150, 0.12);
    color: #70808c;
  }
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  &.status-active {
    background: rgba(6, 214, 160, 0.12);
    color: #06d6a0;

    .status-dot {
      background: #06d6a0;
    }
  }

  &.status-blocked {
    background: rgba(198, 71, 82, 0.12);
    color: #c64752;

    .status-dot {
      background: #c64752;
    }
  }
}

.date-cell {
  color: #70808c;
  font-size: 0.85rem;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.2s ease;

  &--edit {
    background: rgba(0, 168, 150, 0.12);
    color: #00a896;

    &:hover {
      background: #00a896;
      color: white;
    }
  }

  &--block {
    background: rgba(198, 71, 82, 0.12);
    color: #c64752;

    &:hover {
      background: #c64752;
      color: white;
    }
  }

  &--unblock {
    background: rgba(6, 214, 160, 0.12);
    color: #06d6a0;

    &:hover {
      background: #06d6a0;
      color: white;
    }
  }
}

/* === Пагинация === */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.25rem;
  border-top: 1px solid #e8edf0;
}

.pagination-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #e8edf0;
  background: white;
  color: #172f40;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background: #f8fafc;
    border-color: #00a896;
    color: #00a896;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.pagination-info {
  color: #70808c;
  font-size: 0.88rem;
  font-weight: 600;
}

/* === Анимации === */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* === Адаптивность === */
@media (max-width: 991.98px) {
  .users-table {
    th, td {
      padding: 0.75rem;
    }
  }

  .contacts-cell {
    display: none;
  }
}

@media (max-width: 767.98px) {
  .page-header {
    flex-direction: column;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .users-table {
    font-size: 0.85rem;

    th:nth-child(4),
    td:nth-child(4),
    th:nth-child(5),
    td:nth-child(5) {
      display: none;
    }
  }
}

.btn-export {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  background: linear-gradient(135deg, #1d6f42, #155732);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(29, 111, 66, 0.25);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(29, 111, 66, 0.35);
  }

  i {
    color: #a3e635;
  }
}

.role-badge-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    i {
      transform: rotate(180deg);
    }
  }

  i {
    font-size: 0.65rem;
    transition: transform 0.2s ease;
  }

  &.role-admin { background: rgba(111, 66, 193, 0.12); color: #6f42c1; }
  &.role-manager { background: rgba(13, 202, 240, 0.12); color: #0dcaf0; }
  &.role-moderator { background: rgba(253, 126, 20, 0.12); color: #fd7e14; }
  &.role-executor { background: rgba(0, 168, 150, 0.12); color: #00a896; }
  &.role-user { background: rgba(113, 128, 150, 0.12); color: #70808c; }
}
</style>