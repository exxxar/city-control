<!-- client/src/components/media/MediaUploader.vue -->
<template>
  <div class="media-uploader">
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      :multiple="multiple"
      class="d-none"
      @change="handleFileSelect"
    >

    <button type="button" class="btn btn-outline-secondary w-100 mb-3" @click="triggerFileInput">
      <IconFa name="camera" class="me-2" />
      Добавить фото/видео
    </button>

    <div v-if="files.length > 0" class="preview-grid d-flex flex-wrap gap-2">
      <div v-for="(file, index) in files" :key="index" class="preview-item position-relative">
        <img v-if="file.preview" :src="file.preview" class="preview-img rounded" alt="Preview">
        <div v-else class="preview-placeholder bg-light rounded d-flex align-items-center justify-content-center">
          <IconFa name="file-earmark" size="2rem" color="#6c757d" />
        </div>

        <button
          type="button"
          class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1 rounded-circle"
          style="width: 24px; height: 24px; padding: 0;"
          @click="removeFile(index)"
        >
          <IconFa name="x" size="0.75rem" />
        </button>

        <div v-if="file.progress > 0 && file.progress < 100" class="progress-overlay">
          <div class="progress" style="height: 4px;">
            <div class="progress-bar" :style="{ width: file.progress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'MediaUploader',
  components: { IconFa },
  props: {
    accept: { type: String, default: 'image/*,video/*' },
    multiple: { type: Boolean, default: true },
    maxFiles: { type: Number, default: 10 }
  },
  emits: ['files-selected', 'file-removed'],
  data() {
    return {
      files: []
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileSelect(event) {
      const selectedFiles = Array.from(event.target.files)

      selectedFiles.forEach(file => {
        if (this.files.length >= this.maxFiles) return

        const preview = file.type.startsWith('image/') ? URL.createObjectURL(file) : null

        this.files.push({
          file,
          preview,
          name: file.name,
          size: file.size,
          type: file.type,
          progress: 0
        })
      })

      this.$emit('files-selected', this.files.map(f => f.file))
      event.target.value = '' // Сброс для повторного выбора
    },
    removeFile(index) {
      const file = this.files[index]
      if (file.preview) URL.revokeObjectURL(file.preview)
      this.files.splice(index, 1)
      this.$emit('file-removed', this.files.map(f => f.file))
    }
  }
}
</script>

<style scoped>
.preview-item {
  width: 100px;
  height: 100px;
  position: relative;
}

.preview-img, .preview-placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.progress-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 4px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0 0 4px 4px;
}
</style>