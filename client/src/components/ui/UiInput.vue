<!-- client/src/components/ui/UiInput.vue -->
<template>
  <div class="mb-3">
    <label v-if="label" :for="inputId" class="form-label">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>

    <div class="input-group" :class="{ 'has-validation': error }">
      <span v-if="prependIcon" class="input-group-text">
        <i :class="prependIcon"></i>
      </span>

      <input
        :id="inputId"
        ref="input"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :maxlength="maxlength"
        :class="['form-control', { 'is-invalid': error }]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      >

      <span v-if="appendIcon" class="input-group-text">
        <i :class="appendIcon"></i>
      </span>

      <div v-if="error" class="invalid-feedback">
        {{ error }}
      </div>
    </div>

    <div v-if="hint && !error" class="form-text">
      {{ hint }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'UiInput',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    hint: {
      type: String,
      default: ''
    },
    prependIcon: {
      type: String,
      default: ''
    },
    appendIcon: {
      type: String,
      default: ''
    },
    min: {
      type: [String, Number],
      default: null
    },
    max: {
      type: [String, Number],
      default: null
    },
    step: {
      type: [String, Number],
      default: null
    },
    maxlength: {
      type: [String, Number],
      default: null
    }
  },
  emits: ['update:modelValue', 'blur', 'focus'],
  computed: {
    inputId() {
      return `input-${this._.uid}`
    }
  },
  methods: {
    focus() {
      this.$refs.input?.focus()
    }
  }
}
</script>

<style scoped>
.form-control:focus {
  border-color: var(--civic-primary, #00A896);
  box-shadow: 0 0 0 0.25rem rgba(0, 168, 150, 0.25);
}

.input-group-text {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}
</style>