<!-- client/src/components/problems/ProblemAttachments.vue -->
<template>
  <div class="problem-attachments">
    <h6 class="fw-bold mb-3">
      <IconFa name="paperclip" class="me-2" /> Вложения ({{ attachments.length }})
    </h6>

    <div v-if="attachments.length === 0" class="text-center text-muted py-4">
      <IconFa name="image" size="3rem" class="mb-2" />
      <p>Нет вложений</p>
    </div>

    <div v-else class="attachments-grid d-flex flex-wrap gap-2">
      <div
        v-for="att in attachments"
        :key="att.id"
        class="attachment-item position-relative"
        @click="openLightbox(att)"
      >
        <img v-if="isImage(att)" :src="att.file_url" class="attachment-thumb rounded" :alt="att.file_name">
        <div v-else class="attachment-placeholder bg-light rounded d-flex align-items-center justify-content-center">
          <IconFa :name="getFileIcon(att)" size="2rem" color="#6c757d" />
        </div>

        <div class="attachment-overlay">
          <IconFa name="eye" size="1.25rem" color="white" />
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <UiModal v-model="showLightbox" size="lg" :closable="true">
      <div v-if="selectedAttachment" class="text-center">
        <img v-if="isImage(selectedAttachment)" :src="selectedAttachment.file_url" class="img-fluid rounded" :alt="selectedAttachment.file_name">
        <div v-else class="py-5">
          <IconFa :name="getFileIcon(selectedAttachment)" size="5rem" color="#6c757d" />
          <p class="mt-3">{{ selectedAttachment.file_name }}</p>
          <a :href="selectedAttachment.file_url" download class="btn btn-civic">
            <IconFa name="download" class="me-2" /> Скачать
          </a>
        </div>
      </div>
    </UiModal>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import UiModal from '@/components/ui/UiModal.vue'

export default {
  name: 'ProblemAttachments',
  components: { IconFa, UiModal },
  props: {
    attachments: { type: Array, default: () => [] }
  },
  data() {
    return {
      showLightbox: false,
      selectedAttachment: null
    }
  },
  methods: {
    isImage(att) {
      return att.mime_type?.startsWith('image/')
    },
    getFileIcon(att) {
      if (att.mime_type?.startsWith('video/')) return 'camera-video'
      if (att.mime_type?.includes('pdf')) return 'file-pdf'
      if (att.mime_type?.includes('word') || att.mime_type?.includes('document')) return 'file-word'
      return 'file-earmark'
    },
    openLightbox(att) {
      this.selectedAttachment = att
      this.showLightbox = true
    }
  }
}
</script>

<style scoped>
.attachment-item {
  width: 120px;
  height: 120px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
}

.attachment-thumb, .attachment-placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.attachment-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.attachment-item:hover .attachment-overlay {
  opacity: 1;
}
</style>