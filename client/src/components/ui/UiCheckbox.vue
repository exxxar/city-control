<!-- client/src/components/ui/UiCheckbox.vue -->
<template>
  <div class="form-check mb-2">
    <input
      :id="inputId"
      type="checkbox"
      class="form-check-input"
      :checked="modelValue"
      :disabled="disabled"
      @change="$emit('update:modelValue', $event.target.checked)"
    >
    <label :for="inputId" class="form-check-label">
      {{ label }}
    </label>
  </div>
</template>

<script>
export default {
  name: 'UiCheckbox',
  props: {
    modelValue: { type: Boolean, default: false },
    label: { type: String, default: '' },
    disabled: { type: Boolean, default: false }
  },
  emits: ['update:modelValue'],
  computed: {
    inputId() { return `checkbox-${this._.uid}` }
  }
}
</script>