<!-- client/src/components/reports/FileUploader.vue -->
<template>
  <div class="file-uploader">
    <input type="file" ref="fileInput" multiple class="d-none" @change="handleFiles">
    <button type="button" class="btn btn-outline-secondary w-100 rounded-3" @click="$refs.fileInput.click()">
      <IconFa name="paperclip" class="me-2" /> Прикрепить файлы
    </button>

    <div class="mt-2">
      <div v-for="(file, index) in files" :key="index" class="d-flex align-items-center justify-content-between bg-light rounded-2 p-2 mb-2">
        <div class="d-flex align-items-center overflow-hidden">
          <IconFa name="file" class="me-2 text-muted" />
          <span class="text-truncate small">{{ file.name }}</span>
        </div>
        <button type="button" class="btn btn-sm btn-link text-danger p-0" @click="removeFile(index)">
          <IconFa name="xmark" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'FileUploader',
  components: { IconFa },
  props: {
    modelValue: { type: Array, default: () => [] }
  },
  emits: ['update:modelValue'],
  computed: {
    files: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    }
  },
  methods: {
    handleFiles(e) {
      const newFiles = Array.from(e.target.files)
      this.files = [...this.files, ...newFiles]
      e.target.value = '' // Сброс для повторного выбора того же файла
    },
    removeFile(index) {
      this.files.splice(index, 1)
    }
  }
}
</script>