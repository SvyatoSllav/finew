<template>
  <nav class="fixed bottom-0 w-full z-50 bg-white/90 backdrop-blur-md rounded-t-[36px] shadow-[0_-4px_20px_0_rgba(0,0,0,0.05)] flex justify-around items-center h-20 pb-safe px-2">
    <button
      v-for="tab in tabs"
      :key="tab.name"
      class="flex flex-col items-center justify-center w-16 h-full rounded-xl transition-colors duration-150 active:scale-90"
      :class="isActive(tab) ? 'text-cta' : 'text-neutral-400 hover:text-cta'"
      @click="handleTab(tab)"
    >
      <AppIcon
        :name="tab.icon"
        :fill="isActive(tab) ? 1 : 0"
        class="mb-1"
      />
      <span class="text-[10px] font-medium tracking-wide">{{ tab.label }}</span>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import AppIcon from '@/components/ui/AppIcon.vue'

const emit = defineEmits<{
  'add-transaction': []
}>()

const route = useRoute()
const router = useRouter()

interface Tab {
  name: string
  label: string
  icon: string
  route?: string
  action?: string
}

const tabs: Tab[] = [
  { name: 'dashboard', label: 'Главная', icon: 'home', route: '/dashboard' },
  { name: 'transactions', label: 'Операции', icon: 'receipt_long', route: '/transactions' },
  { name: 'add', label: 'Добавить', icon: 'add_circle', action: 'add-transaction' },
  { name: 'analytics', label: 'Аналитика', icon: 'insights', route: '/analytics' },
  { name: 'profile', label: 'Профиль', icon: 'person', route: '/profile' },
]

function isActive(tab: Tab): boolean {
  if (!tab.route) return false
  return route.path === tab.route
}

function handleTab(tab: Tab) {
  if (tab.action) {
    emit('add-transaction')
  } else if (tab.route) {
    router.push(tab.route)
  }
}
</script>
