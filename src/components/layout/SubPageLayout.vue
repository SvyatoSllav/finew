<template>
  <div class="min-h-screen bg-background flex flex-col">
    <header class="sticky top-0 z-50 flex items-center justify-between px-4 h-16 w-full bg-background/90 backdrop-blur-md">
      <button
        class="p-2 -ml-2 rounded-full text-on-surface hover:bg-surface-container-high transition-colors active:scale-95 duration-200"
        @click="handleBack"
      >
        <AppIcon name="arrow_back" />
      </button>
      <h1 class="text-xl font-semibold text-on-surface tracking-tight">{{ title }}</h1>
      <div class="w-10">
        <slot name="action" />
      </div>
    </header>
    <main class="flex-1 px-4 pb-8 pt-6 max-w-2xl mx-auto w-full">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppIcon from '@/components/ui/AppIcon.vue'

interface Props {
  title: string
}

defineProps<Props>()
const router = useRouter()

function handleBack() {
  router.back()
}
</script>
