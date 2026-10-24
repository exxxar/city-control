<!-- admin/src/components/categories/CategoryEditModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>{{ isEdit ? 'Редактирование' : 'Создание' }} записи</h2>
        <button class="close-btn" @click="$emit('close')"><i class="fas fa-times"></i></button>
      </div>

      <form @submit.prevent="saveItem" class="modal-body">
        <div class="form-group">
          <label class="form-label">Название *</label>
          <input v-model="form.name" type="text" class="form-control-custom" required>
        </div>

        <div class="form-group">
          <label class="form-label">Описание</label>
          <textarea v-model="form.description" rows="3" class="form-control-custom textarea"></textarea>
        </div>

        <div class="form-group" v-if="type !== 'help'">
          <label class="form-label">HTML иконка (Font Awesome)</label>
          <input v-model="form.icon" type="text" class="form-control-custom" placeholder='<i class="fas fa-tag"></i>'>
        </div>

        <div class="form-group" v-if="type !== 'help'">
          <label class="form-label">Варианты (через запятую)</label>
          <textarea v-model="variantsText" rows="3" class="form-control-custom textarea" placeholder="Вариант 1, Вариант 2, Вариант 3"></textarea>
          <small class="form-hint">Будет сохранено как JSON-массив</small>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel" @click="$emit('close')">Отмена</button>
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
import { ref, reactive, computed, watch } from 'vue'
import { useCategoriesStore } from '@/stores/categories.store'

const props = defineProps({
  item: { type: Object, required: true },
  type: { type: String, required: true } // 'problems', 'solutions', 'difficulties', 'help'
})

const emit = defineEmits(['close', 'saved'])

const categoriesStore = useCategoriesStore()
const isSaving = ref(false)

const isEdit = computed(() => props.item.id !== null)

const form = reactive({
  name: props.item.name || '',
  description: props.item.description || '',
  icon: props.item.icon || '<i class="fas fa-tag"></i>',
  variants: props.item.variants || '[]'
})

const variantsText = ref('')

// Инициализация текста вариантов при открытии
watch(() => props.item.variants, (newVal) => {
  if (newVal) {
    try {
      const arr = typeof newVal === 'string' ? JSON.parse(newVal) : newVal
      variantsText.value = arr.join(', ')
    } catch {
      variantsText.value = ''
    }
  }
}, { immediate: true })

async function saveItem() {
  isSaving.value = true
  try {
    // Преобразуем текст вариантов в JSON
    const variantsArray = variantsText.value
        .split(',')
        .map(v => v.trim())
        .filter(v => v.length > 0)

    const payload = {
      ...form,
      variants: JSON.stringify(variantsArray),
      type: props.type === 'problems' ? 0 : props.type === 'solutions' ? 1 : 2
    }

    if (isEdit.value) {
      await categoriesStore.updateCategory(props.item.id, payload)
    } else {
      await categoriesStore.createCategory(payload)
    }

    emit('saved')
  } catch (error) {
    console.error('Save error:', error)
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped lang="scss">
.modal-overlay { position: fixed; inset: 0; background: rgba(23, 47, 64, 0.6); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal-card { background: white; border-radius: 20px; width: 100%; max-width: 550px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 1.75rem; border-bottom: 1px solid #e8edf0; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #172f40; }
.close-btn { width: 36px; height: 36px; border-radius: 10px; border: none; background: #f1f5f9; color: #70808c; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }
.close-btn:hover { background: #e2e8f0; color: #172f40; }

.modal-body { padding: 1.75rem; }
.form-group { margin-bottom: 1.25rem; }
.form-label { display: block; margin-bottom: 0.45rem; color: #172f40; font-size: 0.88rem; font-weight: 700; }
.form-control-custom { width: 100%; border: 1px solid #e8edf0; border-radius: 12px; background: #fcfcfd; padding: 0.75rem 1rem; color: #172f40; font-size: 0.9rem; outline: none; transition: all 180ms ease; }
.form-control-custom:focus { border-color: #00a896; background: white; box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1); }
.form-control-custom.textarea { resize: vertical; min-height: 80px; font-family: inherit; }
.form-hint { display: block; margin-top: 0.35rem; color: #70808c; font-size: 0.78rem; }

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