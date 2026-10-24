<!-- client/src/components/reports/IssueSelector.vue -->
<template>
  <div class="container-fluid p-0">
    <!-- СПИСОК КАТЕГОРИЙ -->
    <template v-if="selected === null">
      <div class="form-floating mb-3">
        <input type="text" class="form-control" id="globalSearch" placeholder="Поиск" v-model="globalSearch">
        <label for="globalSearch">Поиск по категориям</label>
      </div>

      <!-- Результаты поиска -->
      <div v-if="globalSearch.trim() && searchResultsByCategory?.length">
        <div v-for="res in searchResultsByCategory" :key="res.category.id"
             class="card mb-2 shadow-sm rounded-3 border-light-subtle" style="cursor:pointer;" @click="selectCategory(res.category)">
          <div class="card-body">
            <div class="fw-bold mb-2">{{ res.category.name }} <span class="badge bg-primary ms-2">{{ res.matches.length }}</span></div>
            <div class="small text-muted">{{ res.matches.join(', ') }}</div>
          </div>
        </div>
      </div>

      <p v-if="globalSearch.trim() && !searchResultsByCategory?.length" class="alert alert-light text-muted fw-bold">Ничего не найдено</p>

      <!-- Сетка категорий -->
      <template v-if="!globalSearch.trim()">
        <div class="row row-cols-2 g-2">
          <div v-for="item in issues" :key="item.id" class="col">
            <div class="card border-light-subtle shadow-sm rounded-4 h-100" style="min-height:120px; cursor:pointer;" @click="selectCategory(item)">
              <div class="card-body d-flex flex-column justify-content-center align-items-center p-2 position-relative">
                <div style="font-size:32px;" v-html="item.icon || '<i class=\'fa-solid fa-circle-exclamation\'></i>'"></div>
                <div class="text-center fw-bold" style="line-height:1.2; font-size:12px;">{{ item.name }}</div>
                <span v-if="(problems[item.id]?.length || 0) > 0" class="badge bg-primary rounded-3 position-absolute" style="top:8px; right:8px;">
                  {{ problems[item.id].length }}
                </span>
              </div>
            </div>
          </div>
          <!-- Другое -->
          <div class="col">
            <div class="card border-primary shadow-sm rounded-4 h-100" style="min-height:120px; cursor:pointer;" @click="selectCategory('other')">
              <div class="card-body d-flex flex-column justify-content-center align-items-center p-2 position-relative">
                <div style="font-size:32px;"><i class="fa-solid fa-circle-question text-primary"></i></div>
                <div class="text-center fw-bold text-primary" style="line-height:1.2; font-size:12px;">Другое</div>
                <span v-if="(problems[0]?.length || 0) > 0" class="badge bg-primary rounded-3 position-absolute" style="top:8px; right:8px;">
                  {{ problems[0].length }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </template>

    <!-- ДЕТАЛИ КАТЕГОРИИ -->
    <template v-else>
      <div class="d-flex align-items-center mb-3">
        <button type="button" class="btn btn-light me-2 rounded-circle" style="width:36px; height:36px;" @click="selected = null">
          <IconFa name="arrow-left" />
        </button>
        <h5 class="mb-0 fw-bold">{{ selected === 'other' ? 'Другое' : selected.name }}</h5>
      </div>

      <!-- Ввод "Другое" -->
      <template v-if="selected === 'other'">
        <p v-if="!problems[0]?.length" class="alert alert-light text-primary fw-bold">Вы еще ничего не добавили</p>
        <template v-for="(item, index) in (problems[0] || [])" :key="index">
          <div class="input-group mb-2">
            <div class="form-floating flex-grow-1">
              <input type="text" class="form-control" :value="problems[0][index]" @input="updateCustomProblem(index, $event.target.value)" :id="'custom-'+index" placeholder="Текст">
              <label :for="'custom-'+index">Проблема #{{ index + 1 }}</label>
            </div>
            <button type="button" class="btn btn-outline-danger" @click="removeIssue(index)"><IconFa name="trash" /></button>
          </div>
        </template>
        <button type="button" class="btn btn-outline-primary w-100 p-2 rounded-4" :disabled="(problems[0] || []).length >= 10" @click="addAnotherProblem">
          <IconFa name="plus" class="me-1" /> Добавить еще
        </button>
      </template>

      <!-- Выбор вариантов -->
      <template v-else>
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="searchInput" placeholder="Поиск" v-model="search">
          <label for="searchInput">Поиск по вариантам</label>
        </div>

        <div class="list-group shadow-sm rounded-3 overflow-hidden">
          <button type="button" v-for="item in filteredVariants" :key="item"
                  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center p-3 fw-bold"
                  @click="toggleIssue(item)">
            <span>{{ item }}</span>
            <IconFa v-if="(problems[selected.id] || []).includes(item)" name="check" class="text-primary" />
          </button>
          <p v-if="filteredVariants.length === 0" class="list-group-item text-center text-muted py-3">Ничего не найдено</p>
        </div>

        <button type="button" class="btn btn-outline-danger w-100 mt-2 p-2 rounded-4" v-if="(problems[selected.id]?.length || 0) > 0" @click="clearSelected">
          Очистить выбор
        </button>
      </template>
    </template>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'IssueSelector',
  components: { IconFa },
  props: {
    issues: { type: Array, required: true },
    modelValue: { type: Object, default: () => ({}) }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      selected: null,
      globalSearch: '',
      search: ''
    }
  },
  computed: {
    problems: {
      get() { return this.modelValue || {} },
      set(value) { this.$emit('update:modelValue', value) }
    },
    searchResultsByCategory() {
      const q = this.globalSearch.trim().toLowerCase()
      if (!q) return null
      const results = []
      for (const cat of this.issues) {
        const variants = typeof cat.variants === 'string' ? JSON.parse(cat.variants || '[]') : (cat.variants || [])
        const matched = variants.filter(v => v.toLowerCase().includes(q))
        if (matched.length > 0) results.push({ category: cat, matches: matched })
      }
      return results
    },
    filteredVariants() {
      const q = this.search.trim().toLowerCase()
      if (!q) return this.parsedVariants
      return this.parsedVariants.filter(v => v.toLowerCase().includes(q))
    },
    parsedVariants() {
      if (!this.selected?.variants) return []
      try {
        return typeof this.selected.variants === 'string' ? JSON.parse(this.selected.variants) : this.selected.variants
      } catch (e) {
        return []
      }
    }
  },
  methods: {
    selectCategory(item) { this.selected = item },
    toggleIssue(item) {
      const key = this.selected.id
      const next = { ...this.problems }
      if (!next[key]) next[key] = []

      if (next[key].includes(item)) {
        next[key] = next[key].filter(i => i !== item)
      } else {
        next[key] = [...next[key], item]
      }
      if (next[key].length === 0) delete next[key]
      this.problems = next
    },
    clearSelected() {
      if (!this.selected?.id) return
      const next = { ...this.problems }
      delete next[this.selected.id]
      this.problems = next
    },
    addAnotherProblem() {
      const next = { ...this.problems }
      next[0] = [...(next[0] || []), '']
      this.problems = next
    },
    removeIssue(index) {
      const next = { ...this.problems }
      next[0] = [...(next[0] || [])]
      next[0].splice(index, 1)
      if (next[0].length === 0) delete next[0]
      this.problems = next
    },
    updateCustomProblem(index, value) {
      const next = { ...this.problems }
      next[0] = [...(next[0] || [])]
      next[0][index] = value
      this.problems = next
    }
  }
}
</script>