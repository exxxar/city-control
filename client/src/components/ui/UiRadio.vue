<!-- client/src/components/ui/UiRadio.vue -->
<template>
  <div class="form-check mb-2">
    <input
      :id="inputId"
      type="radio"
      class="form-check-input"
      :name="name"
      :value="value"
      :checked="modelValue === value"
      :disabled="disabled"
      @change="$emit('update:modelValue', value)"
    >
    <label :for="inputId" class="form-check-label">
      {{ label }}
    </label>
  </div>
</template>

<script>
export default {
  name: 'UiRadio',
  props: {
    modelValue: { type: [String, Number, Boolean], default: '' },
    value: { type: [String, Number, Boolean], required: true },
    label: { type: String, default: '' },
    name: { type: String, default: '' },
    disabled: { type: Boolean, default: false }
  },
  emits: ['update:modelValue'],
  computed: {
    inputId() { return `radio-${this._.uid}` }
  }
}
</script>