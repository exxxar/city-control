// client/src/composables/useDebounce.js
import { ref, onUnmounted } from 'vue'

export function useDebounce(delay = 300) {
  const timeoutId = ref(null)

  function debounce(fn, ...args) {
    if (timeoutId.value) {
      clearTimeout(timeoutId.value)
    }

    timeoutId.value = setTimeout(() => {
      fn(...args)
      timeoutId.value = null
    }, delay)
  }

  function cancel() {
    if (timeoutId.value) {
      clearTimeout(timeoutId.value)
      timeoutId.value = null
    }
  }

  onUnmounted(() => {
    cancel()
  })

  return {
    debounce,
    cancel
  }
}

export function useDebouncedRef(initialValue, delay = 300) {
  const value = ref(initialValue)
  const debouncedValue = ref(initialValue)
  const { debounce } = useDebounce(delay)

  function setValue(newValue) {
    value.value = newValue
    debounce(() => {
      debouncedValue.value = newValue
    })
  }

  return {
    value,
    debouncedValue,
    setValue
  }
}