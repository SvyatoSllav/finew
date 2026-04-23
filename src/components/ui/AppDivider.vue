<template>
  <div class="flex items-center gap-4 my-6">
    <div class="flex-1 h-px bg-outline-variant"></div>
    <span class="text-xs text-outline">{{ text }}</span>
    <div class="flex-1 h-px bg-outline-variant"></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: 'или',
})
</script>
