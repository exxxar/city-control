<!-- client/src/components/ui/IconFa.vue -->
<template>
  <font-awesome-icon
      :icon="iconArray"
      :style="iconStyle"
      :class="customClass"
  />
</template>

<script>
export default {
  name: 'IconFa',
  props: {
    // Имя иконки в формате "map", "shield-check", "user"
    // Для Font Awesome используем camelCase: "map", "shieldHalved", "user"
    name: {
      type: String,
      required: true
    },
    // Стиль: 'solid' (по умолчанию), 'regular', 'brands'
    style: {
      type: String,
      default: 'solid',
      validator: (v) => ['solid', 'regular', 'brands'].includes(v)
    },
    size: {
      type: String,
      default: '1em'
    },
    color: {
      type: String,
      default: 'currentColor'
    },
    // Дополнительные CSS классы
    class: {
      type: String,
      default: ''
    },
    // Анимация: 'spin', 'pulse', 'beat', 'fade', 'bounce', 'shake'
    animation: {
      type: String,
      default: ''
    }
  },
  computed: {
    iconArray() {
      // Преобразуем имя иконки в массив [стиль, имя]
      // Например: ['fas', 'map'] или ['fab', 'github']
      const prefixMap = {
        solid: 'fas',
        regular: 'far',
        brands: 'fab'
      }
      return [prefixMap[this.style], this.name]
    },
    iconStyle() {
      return {
        fontSize: this.size,
        color: this.color
      }
    },
    customClass() {
      // Добавляем класс анимации если указан
      return this.animation ? `fa-${this.animation}` : ''
    }
  }
}
</script>