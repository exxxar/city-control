<!-- client/src/components/ui/UiPagination.vue -->
<template>
  <nav v-if="totalPages > 1" aria-label="Пагинация" class="mt-4">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <button class="page-link" @click="$emit('update:currentPage', currentPage - 1)">Назад</button>
      </li>
      <li
        v-for="page in visiblePages"
        :key="page"
        class="page-item"
        :class="{ active: page === currentPage, disabled: page === '...' }"
      >
        <button class="page-link" @click="page !== '...' && $emit('update:currentPage', page)">
          {{ page }}
        </button>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <button class="page-link" @click="$emit('update:currentPage', currentPage + 1)">Вперед</button>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'UiPagination',
  props: {
    currentPage: { type: Number, default: 1 },
    totalPages: { type: Number, required: true }
  },
  emits: ['update:currentPage'],
  computed: {
    visiblePages() {
      const pages = [];
      const delta = 2;
      const left = this.currentPage - delta;
      const right = this.currentPage + delta + 1;

      for (let i = 1; i <= this.totalPages; i++) {
        if (i === 1 || i === this.totalPages || (i >= left && i < right)) {
          pages.push(i);
        } else if (pages[pages.length - 1] !== '...') {
          pages.push('...');
        }
      }
      return pages;
    }
  }
}
</script>