<template>
  <div class="px-4 pt-4 space-y-6">
    <!-- Budget Selector -->
    <div class="flex">
      <button class="flex items-center gap-2 bg-surface-container rounded-full px-4 py-2 active:scale-95 duration-200">
        <span class="text-sm text-on-surface-variant font-medium">{{ currentBudgetName }}</span>
        <AppIcon name="keyboard_arrow_down" :size="18" class="text-on-surface-variant" />
      </button>
    </div>

    <!-- Balance Card -->
    <section class="bg-surface-container-lowest rounded-[24px] p-6 shadow-[0_4px_20px_0_rgba(0,0,0,0.05)] border border-stone-100">
      <div class="flex flex-col gap-1">
        <span class="text-xs text-on-surface-variant opacity-70">Баланс</span>
        <h1 class="text-[28px] font-bold text-on-surface tracking-tight">₽ {{ formatAmount(balance) }}</h1>
      </div>
      <div class="grid grid-cols-2 gap-4 mt-6">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center">
            <AppIcon name="arrow_upward" class="text-income" />
          </div>
          <div>
            <p class="text-xs text-on-surface-variant">Доход</p>
            <p class="text-sm font-semibold text-income">₽ {{ formatAmount(totalIncome) }}</p>
          </div>
        </div>
        <div class="flex items-center gap-3 border-l border-stone-100 pl-4">
          <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center">
            <AppIcon name="arrow_downward" class="text-expense" />
          </div>
          <div>
            <p class="text-xs text-on-surface-variant">Расходы</p>
            <p class="text-sm font-semibold text-expense">₽ {{ formatAmount(totalExpenses) }}</p>
          </div>
        </div>
      </div>
      <!-- Period selector -->
      <div class="mt-8 flex bg-surface-container p-1 rounded-full">
        <button
          v-for="period in periods"
          :key="period"
          class="flex-1 py-2 text-sm font-medium rounded-full transition-all"
          :class="selectedPeriod === period ? 'bg-primary text-white shadow-sm' : 'text-on-surface-variant'"
          @click="selectedPeriod = period"
        >
          {{ period }}
        </button>
      </div>
    </section>

    <!-- Category Grid -->
    <section>
      <h2 class="text-lg font-semibold mb-4">Категории расходов</h2>
      <div class="grid grid-cols-4 gap-y-6 gap-x-2">
        <div v-for="cat in categories" :key="cat.id" class="flex flex-col items-center gap-2">
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center"
            :style="{ backgroundColor: (cat.color || '#767869') + '1A' }"
          >
            <AppIcon :name="cat.icon_name" :size="22" :style="{ color: cat.color || '#767869' }" />
          </div>
          <div class="text-center">
            <p class="text-[10px] text-on-surface-variant">{{ cat.name }}</p>
          </div>
        </div>
        <div class="flex flex-col items-center gap-2">
          <div class="w-12 h-12 rounded-full border-2 border-dashed border-stone-300 flex items-center justify-center">
            <AppIcon name="add" class="text-stone-400" :size="22" />
          </div>
          <p class="text-[10px] text-on-surface-variant">Добавить</p>
        </div>
      </div>
    </section>

    <!-- Recent Transactions -->
    <section>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">Последние операции</h2>
        <button class="text-secondary text-sm font-medium" @click="$router.push('/transactions')">Все</button>
      </div>
      <div class="space-y-3">
        <div
          v-for="tx in recentTransactions"
          :key="tx.id"
          class="bg-surface-container-lowest rounded-2xl p-4 flex items-center gap-4 active:scale-[0.98] transition-transform cursor-pointer"
          @click="$router.push(`/transactions/${tx.id}`)"
        >
          <div class="relative">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center"
              :style="{ backgroundColor: (tx.category_detail?.color || '#767869') + '1A' }"
            >
              <AppIcon :name="tx.category_detail?.icon_name || 'receipt'" :size="20" :style="{ color: tx.category_detail?.color || '#767869' }" />
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold truncate">{{ tx.note || tx.category_detail?.name || 'Операция' }}</p>
            <p class="text-xs text-on-surface-variant">{{ tx.category_detail?.name }} &bull; {{ formatTime(tx.occurred_at) }}</p>
          </div>
          <div class="text-right">
            <p
              class="text-sm font-bold"
              :class="tx.type === 'income' ? 'text-income' : 'text-error'"
            >
              {{ tx.type === 'income' ? '+' : '-' }}₽ {{ formatAmount(tx.amount) }}
            </p>
          </div>
        </div>
        <div v-if="recentTransactions.length === 0" class="text-center py-8 text-on-surface-variant text-sm">
          Пока нет операций
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from '@/api/client'
import AppIcon from '@/components/ui/AppIcon.vue'

const selectedPeriod = ref('Месяц')
const periods = ['Неделя', 'Месяц', 'Год']
const currentBudgetName = ref('Основной')
const categories = ref<any[]>([])
const recentTransactions = ref<any[]>([])
const totalIncome = ref(0)
const totalExpenses = ref(0)
const balance = computed(() => totalIncome.value - totalExpenses.value)

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(Math.abs(amount))
}

function formatTime(dateStr: string): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  try {
    const budgets = await api('/budgets/')
    if (budgets.length > 0) {
      const budget = budgets[0]
      currentBudgetName.value = budget.name

      const [cats, txs] = await Promise.all([
        api(`/categories/?budget=${budget.id}`),
        api(`/transactions/?budget=${budget.id}&ordering=-occurred_at`),
      ])

      categories.value = cats
      recentTransactions.value = txs.slice(0, 5)

      totalIncome.value = txs
        .filter((t: any) => t.type === 'income')
        .reduce((sum: number, t: any) => sum + parseFloat(t.amount), 0)
      totalExpenses.value = txs
        .filter((t: any) => t.type === 'expense')
        .reduce((sum: number, t: any) => sum + parseFloat(t.amount), 0)
    }
  } catch {
    // API may not be available yet
  }
})
</script>
