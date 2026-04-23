<template>
  <span
    class="material-symbols-outlined select-none overflow-hidden"
    :style="{ fontSize: `${size}px`, width: `${size}px`, height: `${size}px`, fontVariationSettings: `'FILL' ${fill}, 'wght' ${weight}, 'GRAD' 0, 'opsz' ${size}` }"
  >
    <slot>{{ name }}</slot>
  </span>
</template>

<script setup lang="ts">
interface Props {
  name?: string
  size?: number
  fill?: 0 | 1
  weight?: number
}

withDefaults(defineProps<Props>(), {
  name: '',
  size: 24,
  fill: 0,
  weight: 400,
})
</script>
