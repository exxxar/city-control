// client/src/services/camera.service.js

class CameraService {
  constructor() {
    this.stream = null
    this.isSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
  }

  async checkPermissions() {
    if (!this.isSupported) return false

    try {
      const result = await navigator.permissions.query({ name: 'camera' })
      return result.state === 'granted'
    } catch (err) {
      // Некоторые браузеры не поддерживают permissions API для камеры
      return null
    }
  }

  async startStream(videoElement, facingMode = 'environment') {
    if (!this.isSupported) {
      throw new Error('Camera API is not supported in this browser')
    }

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      })

      if (videoElement) {
        videoElement.srcObject = this.stream
        await videoElement.play()
      }

      return this.stream
    } catch (err) {
      console.error('[CameraService] Failed to start stream:', err)
      throw new Error('Не удалось получить доступ к камере. Проверьте разрешения.')
    }
  }

  stopStream() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop())
      this.stream = null
    }
  }

  capturePhoto(videoElement, quality = 0.9) {
    if (!videoElement || !this.stream) {
      throw new Error('Camera stream is not active')
    }

    const canvas = document.createElement('canvas')
    canvas.width = videoElement.videoWidth
    canvas.height = videoElement.videoHeight

    const ctx = canvas.getContext('2d')
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height)

    return new Promise((resolve) => {
      canvas.toBlob((blob) => {
        resolve({
          blob,
          url: URL.createObjectURL(blob),
          width: canvas.width,
          height: canvas.height
        })
      }, 'image/jpeg', quality)
    })
  }

  async captureVideo(videoElement, durationMs = 5000) {
    if (!this.stream) {
      throw new Error('Camera stream is not active')
    }

    const mediaRecorder = new MediaRecorder(this.stream, {
      mimeType: 'video/webm;codecs=vp9'
    })

    const chunks = []

    return new Promise((resolve, reject) => {
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data)
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'video/webm' })
        resolve({
          blob,
          url: URL.createObjectURL(blob)
        })
      }

      mediaRecorder.onerror = (err) => reject(err)

      mediaRecorder.start()

      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop()
        }
      }, durationMs)
    })
  }

  async selectFromGallery(accept = 'image/*', multiple = false) {
    return new Promise((resolve) => {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = accept
      input.multiple = multiple

      input.onchange = (e) => {
        const files = Array.from(e.target.files)
        resolve(files)
      }

      input.click()
    })
  }
}

export const cameraService = new CameraService()