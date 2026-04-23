<template>
  <div class="px-4 pt-4 pb-8">
    <h1 class="text-2xl font-semibold text-on-surface mb-4">Операции</h1>

    <!-- Search -->
    <div class="relative mb-4">
      <AppIcon name="search" class="absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none" :size="20" />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск операций"
        class="w-full bg-surface-container-high rounded-full py-3 pl-12 pr-4 text-sm text-on-surface outline-none focus:ring-2 focus:ring-primary border-none placeholder:text-outline"
      />
    </div>

    <!-- Filter pills -->
    <div class="flex items-center gap-2 mb-8 overflow-x-auto hide-scrollbar py-1">
      <button
        v-for="period in periods"
        :key="period"
        class="px-4 py-2 rounded-full text-xs font-semibold tracking-[0.05em] whitespace-nowrap transition-colors"
        :class="selectedPeriod === period
          ? 'bg-primary text-on-primary shadow-sm'
          : 'bg-surface-container-high text-on-surface-variant hover:bg-surface-dim'"
        @click="selectedPeriod = period"
      >
        {{ period }}
      </button>
      <div class="flex-grow"></div>
      <button class="bg-surface-container-high text-on-surface-variant hover:bg-surface-dim p-2 rounded-full flex items-center justify-center shrink-0">
        <AppIcon name="tune" :size="20" />
      </button>
    </div>

    <!-- Transaction Groups -->
    <div class="flex flex-col gap-8">
      <div v-for="group in groupedTransactions" :key="group.label" class="flex flex-col gap-3">
        <div class="sticky top-16 z-40 bg-background/95 backdrop-blur-md py-3 flex justify-between items-end border-b border-surface-container-high">
          <h2 class="text-xl font-semibold text-on-surface">{{ group.label }}</h2>
          <span
            class="text-sm"
            :class="group.total >= 0 ? 'text-primary' : 'text-on-surface-variant'"
          >
            {{ group.total >= 0 ? '+' : '-' }}₽ {{ formatAmount(Math.abs(group.total)) }}
          </span>
        </div>

        <div
          v-for="tx in group.transactions"
          :key="tx.id"
          class="bg-surface-container-lowest rounded-[24px] p-4 shadow-[0_2px_8px_rgba(0,0,0,0.04)] flex items-center justify-between gap-4 active:scale-[0.98] transition-transform cursor-pointer"
          @click="$router.push(`/transactions/${tx.id}`)"
        >
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
              :style="{ backgroundColor: tx.category?.color || '#e4e3d9' }"
            >
              <AppIcon :name="tx.category?.icon_name || 'receipt'" :size="20" />
            </div>
            <div class="flex flex-col min-w-0">
              <span class="text-base truncate">{{ tx.category?.name || 'Операция' }}</span>
              <span class="text-xs text-outline truncate">{{ tx.note || '' }}</span>
            </div>
          </div>
          <div class="flex flex-col items-end gap-1 shrink-0">
            <span class="text-base" :class="tx.type === 'income' ? 'text-primary' : 'text-on-surface'">
              {{ tx.type === 'income' ? '+' : '-' }}₽ {{ formatAmount(tx.amount) }}
            </span>
            <span class="text-xs text-outline">{{ formatTime(tx.occurred_at) }}</span>
          </div>
        </div>
      </div>

      <div v-if="groupedTransactions.length === 0" class="text-center py-12 text-on-surface-variant text-sm">
        Пока нет операций
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import type { Transaction, Category } from '@/types'

const searchQuery = ref('')
const selectedPeriod = ref('Неделя')
const periods = ['Неделя', 'Месяц', 'Год']

// Mock data for now — will be populated from Firestore
const transactions = ref<(Transaction & { category?: Category })[]>([])

interface TransactionGroup {
  label: string
  total: number
  transactions: (Transaction & { category?: Category })[]
}

const groupedTransactions = computed<TransactionGroup[]>(() => {
  // Group by date
  const groups = new Map<string, (Transaction & { category?: Category })[]>()
  for (const tx of transactions.value) {
    const d = tx.occurred_at instanceof Date ? tx.occurred_at : new Date()
    const key = d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key)!.push(tx)
  }
  return Array.from(groups.entries()).map(([label, txs]) => ({
    label,
    total: txs.reduce((sum, t) => sum + (t.type === 'income' ? t.amount : -t.amount), 0),
    transactions: txs,
  }))
})

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(amount)
}

function formatTime(date: Date | any): string {
  if (!date) return ''
  const d = date instanceof Date ? date : new Date()
  return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}
</script>
