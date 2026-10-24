<!-- client/src/components/ui/UiTextarea.vue -->
<template>
  <div class="mb-3">
    <label v-if="label" :for="inputId" class="form-label">{{ label }}</label>
    <textarea
        :id="inputId"
        :value="modelValue"
        :placeholder="placeholder"
        :rows="rows"
        :maxlength="maxlength"
        :class="['form-control', { 'is-invalid': error }]"
        @input="$emit('update:modelValue', $event.target.value)"
    ></textarea>
    <div v-if="error" class="invalid-feedback">{{ error }}</div>
    <div v-if="hint && !error" class="form-text">{{ hint }}</div>
  </div>
</template>

<script>
export default {
  name: 'UiTextarea',
  props: {
    modelValue: { type: String, default: '' },
    label: { type: String, default: '' },
    placeholder: { type: String, default: '' },
    rows: { type: [Number, String], default: 3 },
    maxlength: { type: [Number, String], default: null },
    error: { type: String, default: '' },
    hint: { type: String, default: '' }
  },
  emits: ['update:modelValue'],
  computed: {
    inputId() {
      return `textarea-${this._.uid}`
    }
  }
}
</script>