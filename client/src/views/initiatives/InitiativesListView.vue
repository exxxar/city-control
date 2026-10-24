<!-- client/src/views/initiatives/InitiativesListView.vue -->
<template>
  <div class="initiatives-page">
    <!-- Современный заголовок -->
    <div class="page-header-modern">
      <div>
        <h2 class="page-title">Инициативы граждан</h2>
        <p class="page-subtitle">Голосуйте за идеи и предлагайте свои улучшения для города</p>
      </div>
      <router-link to="/initiatives/create" class="btn-create-modern">
        <IconFa name="plus" class="me-2" />
        <span class="d-none d-sm-inline">Предложить инициативу</span>
        <span class="d-sm-none">Предложить</span>
      </router-link>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-border text-civic" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p class="text-muted small mt-3">Загружаем инициативы...</p>
    </div>

    <!-- Пустое состояние -->
    <div v-else-if="initiatives.length === 0" class="empty-state">
      <div class="empty-icon-wrapper">
        <IconFa name="lightbulb" size="3rem" color="#cbd5e1" />
      </div>
      <h4 class="fw-bold mt-3">Инициатив пока нет</h4>
      <p class="text-muted mb-4">Станьте первым, кто предложит улучшение для нашего города!</p>
      <router-link to="/initiatives/create" class="btn-civic-modern">
        <IconFa name="plus-circle" class="me-2" />
        Предложить инициативу
      </router-link>
    </div>

    <!-- Список инициатив -->
    <div v-else class="initiatives-list">
      <TransitionGroup name="list" tag="div" class="d-flex flex-column gap-3">
        <InitiativeCard
            v-for="initiative in initiatives"
            :key="initiative.id"
            :initiative="initiative"
            @click="openInitiative"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import InitiativeCard from '@/components/initiatives/InitiativeCard.vue'
import { useInitiativesStore } from '@/stores/initiatives.store'

export default {
  name: 'InitiativesListView',
  components: {
    IconFa,
    InitiativeCard
  },
  data() {
    return {
      isLoading: false
    }
  },
  computed: {
    initiativesStore() {
      return useInitiativesStore()
    },
    initiatives() {
      return this.initiativesStore.initiatives
    }
  },
  async mounted() {
    await this.loadInitiatives()
  },
  methods: {
    async loadInitiatives() {
      this.isLoading = true
      try {
        await this.initiativesStore.fetchInitiatives()
      } catch (error) {
        console.error('Failed to load initiatives:', error)
      } finally {
        this.isLoading = false
      }
    },

    openInitiative(initiative) {
      // TODO: Переход на страницу деталей инициативы, когда она будет создана
      // this.$router.push({ name: 'InitiativeDetails', params: { id: initiative.id } })
      console.log('Open initiative:', initiative.id)
    }
  }
}
</script>

<style scoped>
/* === Дизайн-система === */
.initiatives-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.page-header-modern {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0;
}

.page-subtitle {
  color: #70808c;
  font-size: 0.95rem;
  margin: 0.25rem 0 0;
}

.btn-create-modern {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-weight: 700;
  border-radius: 14px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
  transition: all 0.2s ease;
}

.btn-create-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
  color: white;
}

/* === Состояния === */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
}

.loading-state .spinner-border {
  width: 2.5rem;
  height: 2.5rem;
  color: #00a896 !important;
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  background: #ffffff;
  border-radius: 20px;
  border: 1px dashed #e8edf0;
}

.empty-icon-wrapper {
  display: inline-flex;
  width: 80px;
  height: 80px;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 50%;
}

.btn-civic-modern {
  display: inline-flex;
  align-items: center;
  padding: 0.85rem 1.75rem;
  background: linear-gradient(135deg, #00a896, #087e8b);
  color: white;
  font-weight: 700;
  border-radius: 14px;
  text-decoration: none;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 168, 150, 0.25);
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-civic-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.35);
  color: white;
}

/* === Анимации === */
.list-enter-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

/* === Мобильная адаптация === */
@media (max-width: 767.98px) {
  .initiatives-page {
    padding: 1.5rem 1rem;
  }

  .page-header-modern {
    align-items: stretch;
    flex-direction: column;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .btn-create-modern {
    justify-content: center;
    width: 100%;
  }
}
</style>