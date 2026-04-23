<template>
  <div class="px-4 pt-6 pb-8">
    <h1 class="text-2xl font-semibold text-on-background mb-6 text-center">Профиль</h1>

    <!-- Avatar & Info -->
    <section class="flex flex-col items-center mb-8">
      <AppAvatar :name="authStore.user?.display_name || ''" size="lg" />
      <h2 class="text-2xl font-semibold text-on-background mt-4">{{ authStore.user?.display_name || 'Пользователь' }}</h2>
      <p class="text-sm text-on-surface-variant mt-1">{{ authStore.user?.email }}</p>
      <button class="text-tertiary text-base font-medium mt-2">Редактировать</button>
    </section>

    <!-- Budgets -->
    <section class="mb-8">
      <h2 class="text-xl font-semibold text-on-background mb-4">Бюджеты</h2>
      <div class="space-y-4 mb-4">
        <div
          v-for="budget in budgets"
          :key="budget.id"
          class="bg-surface-container-lowest rounded-[24px] p-6 shadow-[0_4px_20px_rgba(0,0,0,0.04)] cursor-pointer active:scale-[0.98] transition-transform"
          @click="$router.push(`/budget/${budget.id}/settings`)"
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-base font-semibold text-on-surface">{{ budget.name }}</h3>
              <p class="text-sm text-on-surface-variant">{{ budget.currency }}</p>
            </div>
            <span class="bg-primary-container text-on-primary-container px-3 py-1 rounded-full text-xs font-semibold tracking-[0.05em]">
              Владелец
            </span>
          </div>
          <div class="flex items-center">
            <div class="flex -space-x-3">
              <AppAvatar v-for="member in budget.members?.slice(0, 3)" :key="member.id" :name="member.user?.display_name || ''" size="sm" border />
            </div>
            <span v-if="(budget.members?.length || 0) > 1" class="ml-3 text-xs text-on-surface-variant">
              +{{ (budget.members?.length || 1) - 1 }} участник
            </span>
          </div>
        </div>
      </div>
      <button
        class="w-full px-6 py-3 rounded-xl border border-tertiary text-tertiary text-base font-medium flex items-center justify-center hover:bg-tertiary hover:text-on-tertiary transition-colors"
      >
        <AppIcon name="add" class="mr-2" />
        Создать бюджет
      </button>
    </section>

    <!-- Settings -->
    <section class="bg-surface-container-lowest rounded-[24px] shadow-[0_4px_20px_rgba(0,0,0,0.04)] overflow-hidden">
      <ul class="divide-y divide-surface-container-highest">
        <li
          v-for="item in settingsItems"
          :key="item.label"
          class="p-4 hover:bg-surface-container-low transition-colors cursor-pointer flex items-center justify-between"
        >
          <div class="flex items-center text-on-surface">
            <AppIcon :name="item.icon" class="mr-3 text-on-surface-variant" />
            <span class="text-base">{{ item.label }}</span>
          </div>
          <AppIcon name="chevron_right" class="text-outline" :size="20" />
        </li>
        <li
          class="p-4 hover:bg-error-container transition-colors cursor-pointer flex items-center"
          @click="handleLogout"
        >
          <div class="flex items-center text-error">
            <AppIcon name="logout" class="mr-3" />
            <span class="text-base">Выйти</span>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import AppIcon from '@/components/ui/AppIcon.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import { useAuth } from '@/composables/useAuth'

const { logout, fetchMe } = useAuth()
const authStore = useAuthStore()
const budgets = ref<any[]>([])

const settingsItems = [
  { label: 'Валюта по умолчанию', icon: 'currency_exchange' },
  { label: 'Уведомления', icon: 'notifications' },
  { label: 'Тема', icon: 'palette' },
  { label: 'О приложении', icon: 'info' },
]

async function handleLogout() {
  await logout()
}

onMounted(async () => {
  if (!authStore.user) {
    await fetchMe()
  }

  try {
    budgets.value = await api('/budgets/')
  } catch {
    // API may not be available
  }
})
</script>
