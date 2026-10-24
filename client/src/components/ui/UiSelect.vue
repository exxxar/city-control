<!-- client/src/components/ui/UiSelect.vue -->
<template>
  <div class="mb-3">
    <label v-if="label" :for="inputId" class="form-label">{{ label }}</label>
    <select
      :id="inputId"
      :value="modelValue"
      :class="['form-select', { 'is-invalid': error }]"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option v-if="placeholder" value="" disabled selected>{{ placeholder }}</option>
      <slot></slot>
    </select>
    <div v-if="error" class="invalid-feedback">{{ error }}</div>
  </div>
</template>

<script>
export default {
  name: 'UiSelect',
  props: {
    modelValue: { type: [String, Number], default: '' },
    label: { type: String, default: '' },
    placeholder: { type: String, default: '' },
    error: { type: String, default: '' }
  },
  emits: ['update:modelValue'],
  computed: {
    inputId() { return `select-${this._.uid}` }
  }
}
</script>