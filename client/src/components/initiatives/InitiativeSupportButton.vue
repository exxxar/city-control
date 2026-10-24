<!-- client/src/components/initiatives/InitiativeSupportButton.vue -->
<template>
  <button
    :class="['btn', isSupported ? 'btn-warning' : 'btn-outline-warning']"
    :disabled="isSupporting"
    @click="toggleSupport"
  >
    <IconFa :name="isSupporting ? 'hourglass-split' : 'hand-thumbs-up-fill'" class="me-2" />
    <span v-if="isSupporting">Поддержка...</span>
    <span v-else-if="isSupported">Поддержано ({{ supportCount }})</span>
    <span v-else>Поддержать ({{ supportCount }})</span>
  </button>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'
import { useInitiativesStore } from '@/stores/initiatives.store'

export default {
  name: 'InitiativeSupportButton',
  components: { IconFa },
  props: {
    initiativeId: { type: Number, required: true },
    initialSupportCount: { type: Number, default: 0 },
    isInitiallySupported: { type: Boolean, default: false }
  },
  data() {
    return {
      isSupported: this.isInitiallySupported,
      supportCount: this.initialSupportCount,
      isSupporting: false
    }
  },
  methods: {
    async toggleSupport() {
      if (this.isSupporting) return

      this.isSupporting = true
      try {
        const initiativesStore = useInitiativesStore()
        await initiativesStore.supportInitiative(this.initiativeId)

        if (this.isSupported) {
          this.supportCount--
        } else {
          this.supportCount++
        }
        this.isSupported = !this.isSupported
      } catch (error) {
        console.error('Failed to toggle support:', error)
      } finally {
        this.isSupporting = false
      }
    }
  }
}
</script>