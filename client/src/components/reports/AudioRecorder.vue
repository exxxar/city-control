<!-- client/src/components/reports/AudioRecorder.vue -->
<template>
  <div class="audio-recorder p-3 bg-light rounded-3">
    <div class="d-flex align-items-center justify-content-between mb-2">
      <span class="fw-bold small">
        <IconFa :name="isRecording ? 'circle-stop text-danger' : 'microphone'" class="me-2" />
        {{ isRecording ? 'Идет запись...' : 'Запись голоса' }}
      </span>
      <span v-if="isRecording" class="badge bg-danger animate-pulse">REC</span>
    </div>

    <div class="d-flex gap-2">
      <button
          v-if="!isRecording && !audioBlob"
          type="button"
          class="btn btn-primary btn-sm flex-grow-1"
          @click="startRecording"
      >
        Начать запись
      </button>

      <button
          v-if="isRecording"
          type="button"
          class="btn btn-danger btn-sm flex-grow-1"
          @click="stopRecording"
      >
        Остановить
      </button>

      <div v-if="audioBlob && !isRecording" class="d-flex gap-2 flex-grow-1">
        <audio :src="audioUrl" controls class="flex-grow-1" style="height: 38px;"></audio>
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="reset">
          <IconFa name="rotate-right" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'AudioRecorder',
  components: { IconFa },
  props: {
    modelValue: { type: Array, default: () => [] }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      audioBlob: null,
      audioUrl: null
    }
  },
  methods: {
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        this.mediaRecorder = new MediaRecorder(stream)
        this.audioChunks = []

        this.mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) this.audioChunks.push(e.data)
        }

        this.mediaRecorder.onstop = () => {
          this.audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' })
          this.audioUrl = URL.createObjectURL(this.audioBlob)
          this.$emit('update:modelValue', [...this.modelValue, this.audioBlob])
          stream.getTracks().forEach(track => track.stop())
        }

        this.mediaRecorder.start()
        this.isRecording = true
      } catch (err) {
        alert('Не удалось получить доступ к микрофону')
      }
    },
    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop()
        this.isRecording = false
      }
    },
    reset() {
      this.audioBlob = null
      this.audioUrl = null
      this.$emit('update:modelValue', [])
    }
  }
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>