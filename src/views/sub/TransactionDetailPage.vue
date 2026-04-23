<template>
  <SubPageLayout title="Детали операции">
    <div class="flex flex-col items-center gap-4 mb-8">
      <div class="w-16 h-16 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shadow-sm">
        <AppIcon name="shopping_cart" :size="32" :fill="1" />
      </div>
      <div class="text-center">
        <h2 class="text-xl font-semibold text-on-surface mb-1">{{ transaction.category_name || 'Операция' }}</h2>
        <p class="text-2xl font-semibold" :class="transaction.type === 'income' ? 'text-income' : 'text-error'">
          {{ transaction.type === 'income' ? '+' : '-' }} ₽ {{ formatAmount(transaction.amount) }}
        </p>
      </div>
    </div>

    <!-- Details card -->
    <section class="bg-surface-container-lowest rounded-2xl p-4 shadow-[0_4px_24px_rgba(0,0,0,0.04)] border border-surface-container-high flex flex-col mb-8">
      <div v-for="(item, i) in detailRows" :key="item.label">
        <div class="flex justify-between items-center py-3">
          <span class="text-sm text-outline">{{ item.label }}</span>
          <component :is="item.component || 'span'" class="text-sm text-on-surface font-medium text-right" v-bind="item.props || {}">
            {{ item.value }}
          </component>
        </div>
        <div v-if="i < detailRows.length - 1" class="w-full h-px bg-surface-container-high"></div>
      </div>
    </section>

    <!-- Actions -->
    <div class="flex flex-col gap-4 mt-auto">
      <button class="w-full border border-tertiary text-tertiary rounded-full py-3.5 flex items-center justify-center gap-2 text-base font-medium hover:bg-tertiary/5 transition-colors active:scale-[0.98]">
        <AppIcon name="edit" :size="18" />
        Редактировать
      </button>
      <button class="w-full border border-error text-error rounded-full py-3.5 flex items-center justify-center gap-2 text-base font-medium hover:bg-error/5 transition-colors active:scale-[0.98]">
        <AppIcon name="delete" :size="18" />
        Удалить
      </button>
    </div>
  </SubPageLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import SubPageLayout from '@/components/layout/SubPageLayout.vue'
import AppIcon from '@/components/ui/AppIcon.vue'

const props = defineProps<{ id: string }>()

// Mock transaction data
const transaction = ref({
  type: 'expense' as const,
  amount: 1200,
  category_name: 'Продукты',
  budget_name: 'Основной',
  user_name: 'Святослав',
  occurred_at: new Date(),
  note: 'Пятёрочка',
})

const detailRows = computed(() => [
  { label: 'Тип', value: transaction.value.type === 'expense' ? 'Расход' : 'Доход' },
  { label: 'Категория', value: transaction.value.category_name },
  { label: 'Бюджет', value: transaction.value.budget_name },
  { label: 'Кто внёс', value: transaction.value.user_name },
  {
    label: 'Дата',
    value: transaction.value.occurred_at.toLocaleDateString('ru-RU', {
      day: 'numeric', month: 'long', year: 'numeric',
    }) + ', ' + transaction.value.occurred_at.toLocaleTimeString('ru-RU', {
      hour: '2-digit', minute: '2-digit',
    }),
  },
  { label: 'Заметка', value: transaction.value.note || '—' },
])

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('ru-RU').format(amount)
}
</script>
