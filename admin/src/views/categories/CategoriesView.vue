<!-- admin/src/views/categories/CategoriesView.vue -->
<template>
  <div class="categories-page">
    <!-- Заголовок -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Справочники</h1>
        <p class="page-subtitle">Управление категориями проблем, решений и форматов помощи</p>
      </div>
      <button class="btn-primary" @click="openCreateModal">
        <i class="fas fa-plus"></i> Добавить запись
      </button>
    </div>

    <!-- Уведомление о моковых данных -->
    <Transition name="fade">
      <div v-if="categoriesStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные. API справочников на бэкенде пока не настроен.</span>
      </div>
    </Transition>

    <!-- Табы -->
    <div class="tabs-container">
      <div class="tabs">
        <button
            v-for="tab in tabs"
            :key="tab.value"
            class="tab-btn"
            :class="{ active: activeTab === tab.value }"
            @click="activeTab = tab.value"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Контент табов -->
    <div class="content-card">
      <div v-if="categoriesStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка справочника...</p>
      </div>

      <div v-else-if="currentItems.length === 0" class="empty-state">
        <i class="fas fa-folder-open"></i>
        <h3>Записи не найдены</h3>
        <p>Нажмите "Добавить запись", чтобы создать первую</p>
      </div>

      <div v-else class="items-grid">
        <div v-for="item in currentItems" :key="item.id" class="item-card">
          <div class="item-header">
            <div class="item-icon" v-html="item.icon || '<i class=\'fas fa-tag\'></i>'"></div>
            <div class="item-actions">
              <button class="icon-btn" @click="openEditModal(item)" title="Редактировать">
                <i class="fas fa-pen"></i>
              </button>
              <button class="icon-btn icon-btn--danger" @click="confirmDelete(item)" title="Удалить">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>

          <h3 class="item-title">{{ item.name }}</h3>
          <p class="item-desc">{{ item.description || 'Нет описания' }}</p>

          <div v-if="item.variants" class="item-variants">
            <span class="variants-label">Варианты:</span>
            <div class="variants-list">
              <span v-for="(v, idx) in parseVariants(item.variants)" :key="idx" class="variant-tag">
                {{ v }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно создания/редактирования -->
    <CategoryEditModal
        v-if="editingItem"
        :item="editingItem"
        :type="activeTab"
        @close="editingItem = null"
        @saved="onItemSaved"
    />

    <!-- Модальное окно подтверждения удаления -->
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
import { ref, computed, onMounted, watch } from 'vue'
import { useCategoriesStore } from '@/stores/categories.store'
import { useNotifications } from '@/composables/useNotifications'
import CategoryEditModal from '@/components/categories/CategoryEditModal.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'

const categoriesStore = useCategoriesStore()
const { success, error: showError } = useNotifications()

const activeTab = ref('problems')
const editingItem = ref(null)
const confirmAction = ref(null)

const tabs = [
  { value: 'problems', label: 'Категории проблем', icon: 'fas fa-triangle-exclamation' },
  { value: 'solutions', label: 'Варианты решений', icon: 'fas fa-check-circle' },
  { value: 'difficulties', label: 'Трудности', icon: 'fas fa-circle-exclamation' },
  { value: 'help', label: 'Форматы помощи', icon: 'fas fa-hand-holding-heart' }
]

const currentItems = computed(() => {
  if (activeTab.value === 'help') {
    return categoriesStore.helpFormats
  }
  return categoriesStore[activeTab.value] || []
})

function parseVariants(variantsStr) {
  if (!variantsStr) return []
  try {
    return typeof variantsStr === 'string' ? JSON.parse(variantsStr) : variantsStr
  } catch {
    return []
  }
}

function openCreateModal() {
  editingItem.value = {
    id: null,
    name: '',
    description: '',
    icon: '<i class="fas fa-tag"></i>',
    variants: '[]',
    type: activeTab.value === 'problems' ? 0 : activeTab.value === 'solutions' ? 1 : 2
  }
}

function openEditModal(item) {
  editingItem.value = { ...item }
}

async function onItemSaved() {
  editingItem.value = null
  await loadData()
  success('Запись успешно сохранена')
}

function confirmDelete(item) {
  confirmAction.value = {
    title: 'Удаление записи',
    message: `Вы уверены, что хотите удалить "${item.name}"? Это действие нельзя отменить.`,
    callback: async () => {
      try {
        if (activeTab.value === 'help') {
          // TODO: API удаления форматов помощи
          categoriesStore.helpFormats = categoriesStore.helpFormats.filter(f => f.id !== item.id)
        } else {
          await categoriesStore.deleteCategory(item.id)
        }
        success('Запись удалена')
        confirmAction.value = null
      } catch (err) {
        showError('Ошибка при удалении')
      }
    }
  }
}

async function loadData() {
  if (activeTab.value === 'help') {
    await categoriesStore.fetchHelpFormats()
  } else {
    const typeMap = { problems: 0, solutions: 1, difficulties: 2 }
    await categoriesStore.fetchCategories(typeMap[activeTab.value])
  }
}

watch(activeTab, () => {
  loadData()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.categories-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

.btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #00a896, #087e8b); color: white; border: none; border-radius: 12px; font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.tabs-container { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 0.5rem; }
.tabs { display: flex; gap: 0.5rem; overflow-x: auto; }
.tab-btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; border: none; background: transparent; color: #70808c; font-size: 0.9rem; font-weight: 600; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; white-space: nowrap; }
.tab-btn:hover { background: #f1f5f9; color: #172f40; }
.tab-btn.active { background: linear-gradient(135deg, #00a896, #087e8b); color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }

.content-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; min-height: 400px; }
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; color: #70808c; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state i { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; }

.items-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }

.item-card { background: #f8fafc; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; transition: all 0.2s ease; }
.item-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(23, 47, 64, 0.08); border-color: #00a896; }

.item-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.item-icon { width: 48px; height: 48px; border-radius: 12px; background: white; border: 1px solid #e8edf0; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; color: #00a896; }
.item-actions { display: flex; gap: 0.5rem; }
.icon-btn { width: 32px; height: 32px; border-radius: 8px; border: none; background: white; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.icon-btn:hover { background: #e2e8f0; color: #172f40; }
.icon-btn--danger:hover { background: #fee2e2; color: #c64752; }

.item-title { margin: 0 0 0.5rem; font-size: 1.1rem; font-weight: 800; color: #172f40; }
.item-desc { margin: 0 0 1rem; color: #70808c; font-size: 0.88rem; line-height: 1.5; }

.item-variants { padding-top: 1rem; border-top: 1px solid #e8edf0; }
.variants-label { display: block; font-size: 0.78rem; font-weight: 700; color: #70808c; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
.variants-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.variant-tag { padding: 0.35rem 0.75rem; background: white; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.78rem; color: #172f40; font-weight: 600; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 767.98px) {
  .items-grid { grid-template-columns: 1fr; }
  .tabs { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 0.5rem; }
}
</style>