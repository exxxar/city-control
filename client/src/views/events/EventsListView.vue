<!-- client/src/views/events/EventsListView.vue -->
<template>
  <div class="events-page">
    <!-- Современный заголовок -->
    <div class="page-header-modern">
      <div>
        <h2 class="page-title">Мероприятия</h2>
        <p class="page-subtitle">Управляйте заявками и отслеживайте статус событий</p>
      </div>
      <router-link to="/events/create" class="btn-create-modern">
        <IconFa name="plus" class="me-2" />
        <span class="d-none d-sm-inline">Новая заявка</span>
        <span class="d-sm-none">Создать</span>
      </router-link>
    </div>

    <!-- Фильтры -->
    <div class="filters-bar mb-4">
      <div class="row g-3">
        <div class="col-12 col-md-6">
          <div class="input-wrapper">
            <span class="input-icon"><IconFa name="filter" /></span>
            <select v-model="filters.status" class="form-control-custom form-select-custom">
              <option value="">Все статусы</option>
              <option value="approved">Согласованные</option>
              <option value="scheduled">Запланированные</option>
              <option value="completed">Завершённые</option>
              <option value="pending_approval">На согласовании</option>
            </select>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="input-wrapper">
            <span class="input-icon"><IconFa name="calendar-days" /></span>
            <select v-model="filters.period" class="form-control-custom form-select-custom">
              <option value="">Все периоды</option>
              <option value="upcoming">Ближайшие</option>
              <option value="this_month">Этот месяц</option>
              <option value="past">Прошедшие</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-border text-civic" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p class="text-muted small mt-3">Загружаем мероприятия...</p>
    </div>

    <!-- Пустое состояние -->
    <div v-else-if="events.length === 0" class="empty-state">
      <div class="empty-icon-wrapper">
        <IconFa name="calendar-xmark" size="3rem" color="#cbd5e1" />
      </div>
      <h4 class="fw-bold mt-3">Мероприятий пока нет</h4>
      <p class="text-muted mb-4">
        {{ filters.status || filters.period ? 'Попробуйте изменить параметры фильтрации' : 'Вы еще не создали ни одной заявки. Самое время это исправить!' }}
      </p>
      <router-link v-if="!filters.status && !filters.period" to="/events/create" class="btn-civic-modern">
        <IconFa name="plus-circle" class="me-2" />
        Подать первую заявку
      </router-link>
      <button v-else @click="resetFilters" class="btn-civic-modern">
        <IconFa name="rotate-left" class="me-2" />
        Сбросить фильтры
      </button>
    </div>

    <!-- Список мероприятий -->
    <div v-else class="events-list">
      <TransitionGroup name="list" tag="div" class="d-flex flex-column gap-3">
        <EventCard
            v-for="event in events"
            :key="event.id"
            :event="event"
            @click="openEvent"
        />
      </TransitionGroup>

      <!-- Пагинация -->
      <div v-if="pagination.pages > 1" class="pagination-wrapper mt-4">
        <UiPagination
            :current-page="pagination.page"
            :total-pages="pagination.pages"
            @update:current-page="changePage"
        />
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import UiPagination from '@/components/ui/UiPagination.vue'
import EventCard from '@/components/events/EventCard.vue'
import { useEventsStore } from '@/stores/events.store'

export default {
  name: 'EventsListView',
  components: {
    IconFa,
    UiPagination,
    EventCard
  },
  data() {
    return {
      filters: {
        status: '',
        period: ''
      },
      isLoading: false
    }
  },
  computed: {
    eventsStore() {
      return useEventsStore()
    },
    events() {
      return this.eventsStore.events
    },
    pagination() {
      return this.eventsStore.pagination
    }
  },
  watch: {
    filters: {
      handler() {
        this.eventsStore.pagination.page = 1
        this.loadEvents()
      },
      deep: true
    }
  },
  async mounted() {
    await this.loadEvents()
  },
  methods: {
    async loadEvents() {
      this.isLoading = true
      try {
        await this.eventsStore.fetchEvents({
          ...this.filters,
          page: this.pagination.page,
          per_page: this.pagination.per_page
        })
      } catch (error) {
        console.error('Failed to load events:', error)
      } finally {
        this.isLoading = false
      }
    },

    resetFilters() {
      this.filters = { status: '', period: '' }
      this.eventsStore.pagination.page = 1
    },

    changePage(page) {
      this.eventsStore.pagination.page = page
      this.loadEvents()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    openEvent(event) {
      console.log('Open event:', event.id)
    }
  }
}
</script>

<style scoped>
.events-page {
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

.filters-bar {
  background: #ffffff;
  border: 1px solid #e8edf0;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 4px 12px rgba(23, 47, 64, 0.03);
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #e8edf0;
  border-radius: 14px;
  background: #fcfcfd;
  transition: all 180ms ease;
  overflow: hidden;
}

.input-wrapper:focus-within {
  border-color: #00a896;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(0, 168, 150, 0.1);
}

.input-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  flex-shrink: 0;
  color: #70808c;
}

.form-control-custom {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.85rem 1rem 0.85rem 0;
  color: #172f40;
  font-size: 0.95rem;
  width: 100%;
}

.form-control-custom:focus {
  outline: none;
  box-shadow: none;
}

.form-select-custom {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%2370808c' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px 12px;
  padding-right: 2.5rem;
}

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

.list-enter-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 1rem;
}

@media (max-width: 767.98px) {
  .events-page {
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

  .filters-bar {
    padding: 1rem;
  }
}
</style>