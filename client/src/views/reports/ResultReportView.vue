<!-- client/src/views/reports/ResultReportView.vue -->
<template>
  <AppLayout>
    <div class="container py-4">
      <div class="card rounded-4 shadow-sm border-0" style="max-width: 800px; margin: 0 auto;">
        <div class="card-body p-4">

          <div class="text-center mb-4">
            <div class="auth-brand-mark mx-auto mb-3">
              <IconFa name="clipboard-check" size="1.5rem" color="white" />
            </div>
            <h4 class="fw-bold mb-1">Отчёт о выполнении</h4>
            <p class="text-muted small">Заполните итоги и трудности по выбранному обращению</p>
          </div>

          <form @submit.prevent="submitForm">
            <!-- ОСНОВНАЯ ИНФОРМАЦИЯ -->
            <h5 class="fw-bold mb-3 text-dark">Основная информация</h5>

            <div class="form-floating mb-3">
              <select class="form-select" v-model="form.report_id" required>
                <option value="" disabled>Выберите обращение</option>
                <option v-for="r in reports" :key="r.id" :value="r.id">
                  Обращение #{{ r.public_id || r.id }} ({{ r.title }})
                </option>
              </select>
              <label>Обращение *</label>
            </div>

            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="form.topic" placeholder="Тема" required>
              <label>Тема отчёта *</label>
            </div>

            <div class="form-floating mb-3">
              <textarea class="form-control" style="height: 120px" v-model="form.description" placeholder="Описание" required></textarea>
              <label>Подробное описание *</label>
            </div>

            <hr class="my-4 text-muted opacity-25">

            <!-- ДЕЙСТВИЯ -->
            <h5 class="fw-bold mb-3 text-dark">Выполненные действия</h5>

            <div v-if="categoriesStore.isLoading" class="text-center py-4">
              <div class="spinner-border text-civic"></div>
            </div>

            <div v-else class="row g-2 mb-3">
              <template v-for="item in visibleActions" :key="item.id">
                <div class="col-6 col-md-4">
                  <div class="nuance-tile" :class="{ active: form.actions.includes(item.id) }" @click="toggleSelection('actions', item.id)">
                    <IconFa :name="item.icon || 'circle'" size="1.5rem" class="mb-2" :color="form.actions.includes(item.id) ? 'var(--civic-primary)' : '#6c757d'" />
                    <div class="tile-title">{{ item.name }}</div>
                  </div>
                </div>
              </template>
            </div>

            <button v-if="actionsHiddenCount > 0" type="button" class="btn btn-outline-secondary btn-sm w-100 mb-4 rounded-3" @click="showMore('actions')">
              <IconFa name="chevron-down" class="me-1" /> Показать ещё ({{ actionsHiddenCount }})
            </button>

            <hr class="my-4 text-muted opacity-25">

            <!-- РЕЗУЛЬТАТ -->
            <h5 class="fw-bold mb-3 text-dark">Достигнутый результат</h5>

            <div v-if="categoriesStore.isLoading" class="text-center py-4">
              <div class="spinner-border text-civic"></div>
            </div>

            <div class="row g-2 mb-3"  v-else>
              <template v-for="item in visibleResult" :key="item.id">
                <div class="col-6 col-md-4">
                  <div class="nuance-tile" :class="{ active: form.result.includes(item.id) }" @click="toggleSelection('result', item.id)">
                    <IconFa :name="item.icon || 'circle'" size="1.5rem" class="mb-2" :color="form.result.includes(item.id) ? 'var(--civic-primary)' : '#6c757d'" />
                    <div class="tile-title">{{ item.name }}</div>
                  </div>
                </div>
              </template>
            </div>

            <button v-if="resultHiddenCount > 0" type="button" class="btn btn-outline-secondary btn-sm w-100 mb-4 rounded-3" @click="showMore('result')">
              <IconFa name="chevron-down" class="me-1" /> Показать ещё ({{ resultHiddenCount }})
            </button>

            <hr class="my-4 text-muted opacity-25">

            <!-- ТРУДНОСТИ -->
            <h5 class="fw-bold mb-3 text-dark">Возникшие трудности</h5>

            <div v-if="categoriesStore.isLoading" class="text-center py-4">
              <div class="spinner-border text-civic"></div>
            </div>

            <div class="row g-2 mb-4" v-else>
              <template v-for="item in visibleDifficulties" :key="item.id">
                <div class="col-6 col-md-4">
                  <div class="nuance-tile" :class="{ active: form.difficulties.includes(item.id) }" @click="toggleSelection('difficulties', item.id)">
                    <IconFa :name="item.icon || 'circle'" size="1.5rem" class="mb-2" :color="form.difficulties.includes(item.id) ? 'var(--civic-primary)' : '#6c757d'" />
                    <div class="tile-title">{{ item.name }}</div>
                  </div>
                </div>
              </template>
            </div>

            <button v-if="difficultiesHiddenCount > 0" type="button" class="btn btn-outline-secondary btn-sm w-100 mb-4 rounded-3" @click="showMore('difficulties')">
              <IconFa name="chevron-down" class="me-1" /> Показать ещё ({{ difficultiesHiddenCount }})
            </button>

            <!-- Кнопка отправки -->
            <button type="submit" class="btn btn-civic w-100 p-3 rounded-4 fw-bold" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              {{ isSubmitting ? 'Сохранение...' : 'Сохранить отчёт' }}
            </button>

          </form>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/layouts/AppLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'
import { useCategoriesStore } from '@/stores/categories.store'
import api from '@/api/http'

export default {
  name: 'ResultReportView',
  components: { AppLayout, IconFa },
  data() {
    return {
      form: {
        report_id: '',
        topic: '',
        description: '',
        actions: [],
        result: [],
        difficulties: []
      },
      reports: [],
      isLoading: false,
      errors: {},
      limit: {
        actions: 9,
        result: 9,
        difficulties: 9
      }
    }
  },
  computed: {
    categoriesStore() { return useCategoriesStore() },

    actionsList() {
      return this.categoriesStore.solutions
    },
    resultList() {
      return this.categoriesStore.solutions
    },
    difficultiesList() {
      return this.categoriesStore.difficulties
    },

    visibleActions() {
      return this.actionsList.slice(0, this.limit.actions)
    },
    visibleResult() {
      return this.resultList.slice(0, this.limit.result)
    },
    visibleDifficulties() {
      return this.difficultiesList.slice(0, this.limit.difficulties)
    },

    actionsHiddenCount() {
      return Math.max(0, this.actionsList.length - this.limit.actions)
    },
    resultHiddenCount() {
      return Math.max(0, this.resultList.length - this.limit.result)
    },
    difficultiesHiddenCount() {
      return Math.max(0, this.difficultiesList.length - this.limit.difficulties)
    }
  },
  async mounted() {
    await this.categoriesStore.fetchCategories()
    await this.loadReports()
  },
  methods: {
    async loadReports() {
      this.isLoading = true
      try {
        const response = await api.get('/problems/my')
        this.reports = response.data.items || response.data || []
      } catch (error) {
        console.error('Ошибка загрузки обращений:', error)
        this.reports = [
          { id: 1, public_id: 'A1B2C3', title: 'Яма на ул. Ленина' },
          { id: 2, public_id: 'D4E5F6', title: 'Не горит фонарь в парке' }
        ]
      } finally {
        this.isLoading = false
      }
    },

    toggleSelection(field, id) {
      const arr = this.form[field]
      const index = arr.indexOf(id)

      if (index === -1) {
        arr.push(id)
      } else {
        arr.splice(index, 1)
      }
    },

    showMore(field) {
      this.limit[field] += 9
    },

    async submitForm() {
      if (!this.form.report_id || !this.form.topic || !this.form.description) {
        return alert('Пожалуйста, заполните обязательные поля: Обращение, Тему и Описание')
      }

      this.isLoading = true
      try {
        const payload = {
          ...this.form,
          actions: JSON.stringify(this.form.actions),
          result: JSON.stringify(this.form.result),
          difficulties: JSON.stringify(this.form.difficulties)
        }

        await api.post('/result-reports', payload)

        alert('Отчёт успешно сохранён!')
        this.$router.push('/executor/dashboard')
      } catch (error) {
        console.error('Ошибка сохранения отчёта:', error)
        alert('Произошла ошибка при сохранении отчёта. Попробуйте позже.')
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
<style scoped>
.auth-brand-mark {
  display: inline-flex;
  width: 56px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #00a896, #087e8b);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.25);
}

.nuance-tile {
  border: 1px solid #e8edf0;
  border-radius: 12px;
  padding: 16px 8px;
  text-align: center;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.nuance-tile:hover {
  border-color: rgba(0, 168, 150, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.nuance-tile.active {
  border-color: #00a896;
  background: rgba(0, 168, 150, 0.08);
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.15);
}

.tile-title {
  font-size: 0.8rem;
  line-height: 1.3;
  font-weight: 600;
  color: #172f40;
}

.nuance-tile.active .tile-title {
  color: #008f80;
}

.btn-civic {
  background: linear-gradient(135deg, #00a896, #087e8b);
  border: none;
  color: white;
  transition: all 0.2s ease;
}

.btn-civic:hover:not(:disabled) {
  background: linear-gradient(135deg, #008f80, #066a75);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.3);
}

.btn-civic:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-floating > .form-control:focus,
.form-floating > .form-select:focus {
  border-color: #00a896;
  box-shadow: 0 0 0 0.25rem rgba(0, 168, 150, 0.15);
}
</style>