<template>
  <header class="sticky top-0 z-50 flex items-center justify-between px-6 h-16 w-full" style="background-color: #F9EEEE">
    <div class="flex items-center gap-2">
      <span class="text-2xl font-black tracking-tighter" style="color: #F16F33">FineW</span>
    </div>
    <div class="flex items-center gap-4">
      <button class="hover:opacity-80 transition-opacity active:scale-95 duration-200">
        <AppIcon name="notifications" class="text-stone-500" />
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import AppIcon from '@/components/ui/AppIcon.vue'
</script>
