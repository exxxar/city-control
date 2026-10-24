<!-- admin/src/views/categories/IssueCategoriesView.vue -->
<template>
  <div class="issue-categories-page">
    <div class="page-header">
      <div>
        <h1 class="page-title">Категории обращений</h1>
        <p class="page-subtitle">Управление категориями проблем, решений и трудностей</p>
      </div>
      <button class="btn-primary" @click="openCreateModal">
        <i class="fas fa-plus"></i> Добавить категорию
      </button>
    </div>

    <Transition name="fade">
      <div v-if="categoriesStore.isUsingMock" class="mock-notice">
        <i class="fas fa-info-circle"></i>
        <span>Отображаются демо-данные.</span>
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
          <span class="tab-count">{{ getTabCount(tab.value) }}</span>
        </button>
      </div>
    </div>

    <!-- Контент -->
    <div class="content-card">
      <div v-if="categoriesStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка...</p>
      </div>

      <div v-else-if="currentItems.length === 0" class="empty-state">
        <i :class="currentTabIcon"></i>
        <h3>Нет записей в этой категории</h3>
        <p>Нажмите "Добавить категорию", чтобы создать первую</p>
      </div>

      <div v-else class="categories-list">
        <div v-for="item in currentItems" :key="item.id" class="category-item">
          <div class="category-icon" v-html="item.icon || '<i class=\'fas fa-tag\'></i>'"></div>
          <div class="category-info">
            <div class="category-name">{{ item.name }}</div>
            <div class="category-desc">{{ item.description || 'Нет описания' }}</div>
            <div v-if="parseVariants(item.variants).length" class="category-variants">
              <span v-for="(v, idx) in parseVariants(item.variants).slice(0, 5)" :key="idx" class="variant-tag">{{ v }}</span>
              <span v-if="parseVariants(item.variants).length > 5" class="variant-tag variant-tag--more">
                +{{ parseVariants(item.variants).length - 5 }}
              </span>
            </div>
          </div>
          <div class="category-actions">
            <button class="icon-btn" @click="openEditModal(item)" title="Редактировать">
              <i class="fas fa-pen"></i>
            </button>
            <button class="icon-btn icon-btn--danger" @click="confirmDelete(item)" title="Удалить">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модалка редактирования -->
    <IssueCategoryEditModal
        v-if="editingItem"
        :item="editingItem"
        :type="activeTab"
        @close="editingItem = null"
        @saved="onItemSaved"
    />

    <!-- Модалка подтверждения -->
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
import IssueCategoryEditModal from '@/components/categories/IssueCategoryEditModal.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'

const categoriesStore = useCategoriesStore()
const { success, error: showError } = useNotifications()

const activeTab = ref('problems')
const editingItem = ref(null)
const confirmAction = ref(null)

const tabs = [
  { value: 'problems', label: 'Проблемы', icon: 'fas fa-triangle-exclamation', type: 0 },
  { value: 'solutions', label: 'Решения', icon: 'fas fa-check-circle', type: 1 },
  { value: 'difficulties', label: 'Трудности', icon: 'fas fa-circle-exclamation', type: 2 }
]

const currentTabIcon = computed(() => tabs.find(t => t.value === activeTab.value)?.icon || 'fas fa-tag')

const currentItems = computed(() => {
  return categoriesStore[activeTab.value] || []
})

function getTabCount(tabValue) {
  return (categoriesStore[tabValue] || []).length
}

function parseVariants(variantsStr) {
  if (!variantsStr) return []
  try {
    return typeof variantsStr === 'string' ? JSON.parse(variantsStr) : variantsStr
  } catch {
    return []
  }
}

function openCreateModal() {
  const type = tabs.find(t => t.value === activeTab.value)?.type || 0
  editingItem.value = {
    id: null,
    name: '',
    description: '',
    icon: '<i class="fas fa-tag"></i>',
    variants: '[]',
    type
  }
}

function openEditModal(item) {
  editingItem.value = { ...item }
}

async function onItemSaved() {
  editingItem.value = null
  await loadData()
  success('Категория сохранена')
}

function confirmDelete(item) {
  confirmAction.value = {
    title: 'Удаление категории',
    message: `Вы уверены, что хотите удалить "${item.name}"? Это действие нельзя отменить.`,
    callback: async () => {
      try {
        await categoriesStore.deleteCategory(item.id)
        success('Категория удалена')
        confirmAction.value = null
      } catch (err) {
        showError('Ошибка при удалении')
      }
    }
  }
}

async function loadData() {
  const typeMap = { problems: 0, solutions: 1, difficulties: 2 }
  await categoriesStore.fetchCategories(typeMap[activeTab.value])
}

watch(activeTab, () => loadData())

onMounted(() => loadData())
</script>

<style scoped lang="scss">
.issue-categories-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; }
.page-title { margin: 0; font-size: 1.75rem; font-weight: 800; color: #172f40; }
.page-subtitle { margin: 0.25rem 0 0; color: #70808c; font-size: 0.95rem; }

.btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #00a896, #087e8b); color: white; border: none; border-radius: 12px; font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35); }

.mock-notice { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem; background: #fff7df; border: 1px solid rgba(166, 108, 0, 0.2); border-radius: 12px; color: #a66c00; font-size: 0.88rem; font-weight: 600; }

.tabs-container { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 0.5rem; }
.tabs { display: flex; gap: 0.5rem; }
.tab-btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; border: none; background: transparent; color: #70808c; font-size: 0.9rem; font-weight: 600; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; }
.tab-btn:hover { background: #f1f5f9; color: #172f40; }
.tab-btn.active { background: linear-gradient(135deg, #00a896, #087e8b); color: white; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25); }
.tab-count { padding: 0.15rem 0.5rem; background: rgba(255, 255, 255, 0.25); border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
.tab-btn:not(.active) .tab-count { background: #e8edf0; color: #70808c; }

.content-card { background: white; border: 1px solid #e8edf0; border-radius: 16px; padding: 1.5rem; min-height: 400px; }
.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; color: #70808c; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #e8edf0; border-top-color: #00a896; border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state i { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; }

.categories-list { display: flex; flex-direction: column; gap: 0.75rem; }
.category-item { display: flex; gap: 1rem; padding: 1.25rem; background: #f8fafc; border: 1px solid #e8edf0; border-radius: 14px; transition: all 0.2s ease; }
.category-item:hover { border-color: #00a896; box-shadow: 0 4px 16px rgba(23, 47, 64, 0.06); }

.category-icon { width: 52px; height: 52px; border-radius: 12px; background: white; border: 1px solid #e8edf0; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; color: #00a896; flex-shrink: 0; }
.category-info { flex: 1; min-width: 0; }
.category-name { font-weight: 700; color: #172f40; font-size: 1rem; margin-bottom: 0.35rem; }
.category-desc { color: #70808c; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.75rem; }
.category-variants { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.variant-tag { padding: 0.25rem 0.6rem; background: white; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.75rem; color: #172f40; font-weight: 600; }
.variant-tag--more { background: #00a896; color: white; border-color: #00a896; }

.category-actions { display: flex; gap: 0.5rem; align-items: flex-start; }
.icon-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: white; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.icon-btn:hover { background: #e2e8f0; color: #172f40; }
.icon-btn--danger:hover { background: #fee2e2; color: #c64752; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 767.98px) {
  .category-item { flex-direction: column; }
  .category-actions { align-self: flex-end; }
  .tabs { flex-wrap: nowrap; overflow-x: auto; }
}
</style>