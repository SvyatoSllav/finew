<template>
  <div class="px-4 pt-4 pb-8 space-y-8">
    <h1 class="text-2xl font-semibold text-on-surface">Аналитика</h1>

    <!-- Period pills -->
    <div class="space-y-4">
      <div class="bg-surface-container-highest rounded-full p-1 flex items-center shadow-sm">
        <button
          v-for="period in periods"
          :key="period"
          class="flex-1 py-1.5 text-center rounded-full text-xs font-medium transition-all"
          :class="selectedPeriod === period
            ? 'bg-surface-container-lowest text-on-surface font-semibold shadow-sm'
            : 'text-on-surface-variant'"
          @click="selectedPeriod = period"
        >
          {{ period }}
        </button>
      </div>

      <!-- Type toggle -->
      <div class="flex gap-4 border-b border-surface-container-high pb-1">
        <button
          class="text-base pb-1 px-1 transition-colors"
          :class="selectedType === 'expense' ? 'text-primary font-semibold border-b-2 border-primary' : 'text-on-surface-variant'"
          @click="selectedType = 'expense'"
        >
          Расходы
        </button>
        <button
          class="text-base pb-1 px-1 transition-colors"
          :class="selectedType === 'income' ? 'text-primary font-semibold border-b-2 border-primary' : 'text-on-surface-variant'"
          @click="selectedType = 'income'"
        >
          Доходы
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-12 text-on-surface-variant text-sm">Загрузка...</div>

    <template v-else-if="breakdownItems.length > 0">
      <!-- Donut Chart & Breakdown -->
      <section class="bg-surface-container-lowest rounded-[24px] p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)] flex flex-col items-center space-y-8">
        <!-- Donut -->
        <div
          class="relative w-[200px] h-[200px] rounded-full flex items-center justify-center"
          :style="{ background: donutGradient }"
        >
          <div class="absolute inset-[24px] bg-surface-container-lowest rounded-full flex flex-col items-center justify-center shadow-inner">
            <span class="text-xl font-semibold text-on-surface">₽ {{ formatAmount(totalAmount) }}</span>
            <span class="text-xs text-on-surface-variant text-center px-4 mt-1">
              {{ selectedType === 'expense' ? 'Расходы' : 'Доходы' }} за {{ periodLabel }}
            </span>
          </div>
        </div>

        <!-- Breakdown -->
        <div class="w-full space-y-4">
          <div v-for="item in breakdownItems" :key="item.label">
            <div class="flex justify-between items-center mb-1">
              <div class="flex items-center gap-2">
                <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: item.color }"></div>
                <span class="text-sm font-medium text-on-surface">{{ item.label }}</span>
              </div>
              <span class="text-sm font-semibold text-on-surface">
                ₽ {{ formatAmount(item.amount) }}
                <span class="text-xs text-on-surface-variant font-normal ml-1">{{ item.percentage }}%</span>
              </span>
            </div>
            <div class="w-full h-1.5 bg-surface-container rounded-full overflow-hidden">
              <div class="h-full rounded-full" :style="{ width: item.percentage + '%', backgroundColor: item.color }"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- By Members -->
      <section v-if="members.length > 1" class="space-y-4">
        <h2 class="text-xl font-semibold text-on-surface">По участникам</h2>
        <div class="bg-surface-container-lowest rounded-[24px] p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)] space-y-6">
          <div v-for="member in members" :key="member.name" class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <AppAvatar :name="member.name" size="md" />
                <span class="text-base font-medium text-on-surface">{{ member.name }}</span>
              </div>
              <span class="text-base font-semibold text-on-surface">₽ {{ formatAmount(member.amount) }}</span>
            </div>
            <div class="w-full h-2 bg-surface-container rounded-full overflow-hidden">
              <div
                class="h-full rounded-full"
                :style="{ width: member.percentage + '%', backgroundColor: member.color }"
              ></div>
            </div>
          </div>
        </div>
      </section>
    </template>

    <div v-else class="text-center py-12 text-on-surface-variant text-sm">
      Нет данных за выбранный период
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '@/api/client'
import AppAvatar from '@/components/ui/AppAvatar.vue'

const selectedPeriod = ref('Месяц')
const periods = ['Неделя', 'Месяц', 'Год']
const selectedType = ref<'expense' | 'income'>('expense')
const loading = ref(true)
const budgetId = ref('')
const allTransactions = ref<any[]>([])

const memberColors = ['#53621d', '#ff793d', '#0f6667', '#7c3aed', '#dc2626']

const periodLabel = computed(() => {
  if (selectedPeriod.value === 'Неделя') return 'неделю'
  if (selectedPeriod.value === 'Месяц') return 'месяц'
  return 'год'
})

function getPeriodStart(period: string): Date {
  const now = new Date()
  if (period === 'Неделя') {
    return new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7)
  }
  if (period === 'Месяц') {
    return new Date(now.getFullYear(), now.getMonth(), 1)
  }
  return new Date(now.getFullYear(), 0, 1)
}

const filteredTransactions = computed(() => {
  const start = getPeriodStart(selectedPeriod.value)
  return allTransactions.value.filter(t => {
    return t.type === selectedType.value && new Date(t.occurred_at) >= start
  })
})

const breakdownItems = computed(() => {
  const byCategory = new Map<string, { amount: number; color: string }>()

  for (const tx of filteredTransactions.value) {
    const name = tx.category_detail?.name || 'Без категории'
    const color = tx.category_detail?.color || '#767869'
    const existing = byCategory.get(name) || { amount: 0, color }
    existing.amount += parseFloat(tx.amount)
    byCategory.set(name, existing)
  }

  const items = Array.from(byCategory.entries())
    .map(([label, data]) => ({ label, amount: data.amount, color: data.color, percentage: 0 }))
    .sort((a, b) => b.amount - a.amount)

  const total = items.reduce((s, i) => s + i.amount, 0)
  if (total > 0) {
    items.forEach(i => { i.percentage = Math.round((i.amount / total) * 100) })
  }

  return items
})

const totalAmount = computed(() => breakdownItems.value.reduce((s, i) => s + i.amount, 0))

const donutGradient = computed(() => {
  const items = breakdownItems.value
  if (items.length === 0) return 'conic-gradient(#e4e3d9 0% 100%)'
  let cumulative = 0
  const stops = items.map(item => {
    const start = cumulative
    cumulative += item.percentage
    return `${item.color} ${start}% ${cumulative}%`
  })
  return `conic-gradient(${stops.join(', ')})`
})

const members = computed(() => {
  const byMember = new Map<string, number>()

  for (const tx of filteredTransactions.value) {
    const name = tx.user_detail?.display_name || tx.user_detail?.email || 'Участник'
    byMember.set(name, (byMember.get(name) || 0) + parseFloat(tx.amount))
  }

  const items = Array.from(byMember.entries())
    .map(([name, amount], i) => ({ name, amount, color: memberColors[i % memberColors.length], percentage: 0 }))
    .sort((a, b) => b.amount - a.amount)

  const total = items.reduce((s, i) => s + i.amount, 0)
  if (total > 0) {
    items.forEach(i => { i.percentage = Math.round((i.amount / total) * 100) })
  }

  return items
})

async function fetchData() {
  loading.value = true
  try {
    if (!budgetId.value) {
      const budgets = await api('/budgets/')
      if (budgets.length > 0) {
        budgetId.value = budgets[0].id
      } else {
        loading.value = false
        return
      }
    }
    allTransactions.value = await api(`/transactions/?budget=${budgetId.value}&ordering=-occurred_at`)
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(Math.round(amount))
}
</script>
