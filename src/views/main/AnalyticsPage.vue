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
            {{ selectedType === 'expense' ? 'Расходы' : 'Доходы' }} за месяц
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
    <section class="space-y-4">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'

const selectedPeriod = ref('Месяц')
const periods = ['Неделя', 'Месяц', 'Год']
const selectedType = ref<'expense' | 'income'>('expense')

// Mock data
const breakdownItems = ref([
  { label: 'Продукты', amount: 15640, percentage: 45, color: '#ff793d' },
  { label: 'Жилье', amount: 10430, percentage: 30, color: '#53621d' },
  { label: 'Транспорт', amount: 5215, percentage: 15, color: '#0f6667' },
  { label: 'Прочее', amount: 3485, percentage: 10, color: '#bdcf7d' },
])

const totalAmount = computed(() => breakdownItems.value.reduce((s, i) => s + i.amount, 0))

const donutGradient = computed(() => {
  const items = breakdownItems.value
  let cumulative = 0
  const stops = items.map(item => {
    const start = cumulative
    cumulative += item.percentage
    return `${item.color} ${start}% ${cumulative}%`
  })
  return `conic-gradient(${stops.join(', ')})`
})

const members = ref([
  { name: 'Александр', amount: 20500, percentage: 59, color: '#53621d' },
  { name: 'Екатерина', amount: 14270, percentage: 41, color: '#ff793d' },
])

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(amount)
}
</script>
