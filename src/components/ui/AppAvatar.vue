<template>
  <div
    class="rounded-full overflow-hidden flex items-center justify-center shrink-0 bg-surface-container-high text-on-surface-variant font-semibold"
    :class="sizeClasses"
    :style="{ borderWidth: border ? '2px' : '0', borderColor: 'var(--color-surface-container-lowest)' }"
  >
    <img
      v-if="src"
      :src="src"
      :alt="name"
      class="w-full h-full object-cover"
    />
    <span v-else :class="initialsSizeClass">{{ initials }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  src?: string | null
  name?: string
  size?: 'xs' | 'sm' | 'md' | 'lg'
  border?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  src: null,
  name: '',
  size: 'md',
  border: false,
})

const initials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs': return 'w-5 h-5'
    case 'sm': return 'w-8 h-8'
    case 'md': return 'w-10 h-10'
    case 'lg': return 'w-20 h-20'
    default: return 'w-10 h-10'
  }
})

const initialsSizeClass = computed(() => {
  switch (props.size) {
    case 'xs': return 'text-[8px]'
    case 'sm': return 'text-xs'
    case 'md': return 'text-sm'
    case 'lg': return 'text-xl'
    default: return 'text-sm'
  }
})
</script>
