<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'w-full h-14 font-medium text-base rounded-[16px] flex items-center justify-center gap-3 transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none',
      variantClasses,
    ]"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'filled' | 'outlined' | 'text' | 'google' | 'danger'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'filled',
  type: 'button',
  disabled: false,
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'filled':
      return 'bg-cta text-white shadow-lg shadow-cta/20 hover:opacity-95'
    case 'outlined':
      return 'bg-transparent border-2 border-white text-white hover:bg-white/10'
    case 'text':
      return 'bg-transparent text-tertiary hover:bg-tertiary/5'
    case 'google':
      return 'bg-surface-container-lowest border border-outline-variant text-on-surface hover:bg-surface-container-low'
    case 'danger':
      return 'bg-error-container text-on-error-container hover:opacity-90'
    default:
      return ''
  }
})
</script>
