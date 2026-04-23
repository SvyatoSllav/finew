<template>
  <div v-if="variant === 'fullscreen'" class="min-h-screen flex flex-col" style="background-color: #7D8D43">
    <slot />
  </div>
  <div v-else class="min-h-screen flex flex-col" style="background-color: #7D8D43">
    <!-- Green top area -->
    <div class="relative overflow-hidden flex items-center justify-center flex-shrink-0" :class="compact ? 'h-[200px]' : 'h-[353px]'">
      <div class="absolute inset-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <circle cx="20" cy="20" r="40" fill="white" />
          <circle cx="80" cy="80" r="30" fill="white" />
        </svg>
      </div>
      <div class="z-10 flex flex-col items-center">
        <slot name="header">
          <h1 class="text-white text-4xl font-black tracking-tighter">FineW</h1>
          <p class="text-white/80 text-sm mt-2">Финансы для двоих</p>
        </slot>
      </div>
    </div>
    <!-- Cream card -->
    <main class="flex-grow -mt-12 relative z-20">
      <div class="rounded-t-[36px] shadow-2xl min-h-full px-6 pt-8 pb-12 flex flex-col" style="background-color: #F9EEEE">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'fullscreen' | 'card'
  compact?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'card',
  compact: false,
})
</script>
