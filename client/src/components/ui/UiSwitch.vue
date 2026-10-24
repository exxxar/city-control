<!-- client/src/components/ui/UiSwitch.vue -->
<template>
  <div class="form-check form-switch mb-3">
    <input
      :id="inputId"
      type="checkbox"
      class="form-check-input"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
    >
    <label :for="inputId" class="form-check-label">{{ label }}</label>
  </div>
</template>

<script>
export default {
  name: 'UiSwitch',
  props: {
    modelValue: { type: Boolean, default: false },
    label: { type: String, default: '' }
  },
  emits: ['update:modelValue'],
  computed: {
    inputId() { return `switch-${this._.uid}` }
  }
}
</script>