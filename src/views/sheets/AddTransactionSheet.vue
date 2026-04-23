<template>
  <div class="flex flex-col gap-3">
    <!-- Segment Tabs -->
    <div class="flex p-1 bg-surface-container rounded-full w-full max-w-[280px] mx-auto">
      <button
        class="flex-1 py-2 rounded-full text-sm font-medium shadow-sm transition-colors"
        :class="type === 'expense' ? 'bg-error-container text-on-error-container' : 'text-on-surface-variant'"
        @click="type = 'expense'"
      >
        Расход
      </button>
      <button
        class="flex-1 py-2 rounded-full text-sm font-medium transition-colors"
        :class="type === 'income' ? 'bg-primary-fixed text-on-primary-fixed' : 'text-on-surface-variant'"
        @click="type = 'income'"
      >
        Доход
      </button>
    </div>

    <!-- Amount Display -->
    <div class="text-center">
      <span class="text-[40px] leading-[48px] font-bold text-on-surface tracking-tighter">
        ₽ {{ displayAmount }}
      </span>
    </div>

    <!-- Category Grid -->
    <div class="grid grid-cols-4 gap-y-3 gap-x-2">
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="flex flex-col items-center gap-1 group"
        @click="selectedCategory = cat"
      >
        <div
          class="w-11 h-11 rounded-[12px] flex items-center justify-center transition-transform group-active:scale-95"
          :style="selectedCategory?.id === cat.id
            ? { backgroundColor: cat.color || '#53621d', color: '#fff' }
            : { backgroundColor: (cat.color || '#767869') + '1A', color: cat.color || '#767869' }"
        >
          <AppIcon :name="cat.icon_name" :size="20" />
        </div>
        <span
          class="text-[10px] text-center leading-tight"
          :class="selectedCategory?.id === cat.id ? 'text-on-surface font-medium' : 'text-on-surface-variant'"
        >
          {{ cat.name }}
        </span>
      </button>
    </div>

    <!-- Note & Date -->
    <div class="flex gap-2 items-center">
      <div class="flex-1 bg-surface-container-low border border-outline-variant rounded-[20px] px-3 py-2.5 flex items-center gap-2 focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all">
        <AppIcon name="edit" class="text-outline" :size="18" />
        <input
          v-model="note"
          type="text"
          placeholder="Комментарий..."
          class="bg-transparent border-none outline-none w-full text-sm text-on-surface placeholder:text-outline p-0 focus:ring-0"
        />
      </div>
      <button class="bg-surface-container rounded-full px-3 py-2.5 flex items-center gap-1 active:bg-surface-container-high transition-colors">
        <AppIcon name="schedule" class="text-on-surface-variant" :size="16" />
        <span class="text-sm font-medium text-on-surface-variant whitespace-nowrap">Сегодня</span>
      </button>
    </div>

    <!-- Numeric Keypad -->
    <div class="grid grid-cols-3 gap-y-1 gap-x-2 px-4">
      <button
        v-for="key in keypadKeys"
        :key="key"
        class="h-11 text-xl font-semibold text-on-surface rounded-[20px] active:bg-surface-container-high transition-colors flex items-center justify-center"
        @click="handleKey(key)"
      >
        <AppIcon v-if="key === 'backspace'" name="backspace" :size="24" class="text-on-surface" />
        <template v-else>{{ key }}</template>
      </button>
    </div>

    <!-- Add Button -->
    <button
      class="w-full bg-secondary-container text-on-secondary-container rounded-full py-3.5 text-base font-medium shadow-sm active:scale-[0.98] transition-transform flex items-center justify-center disabled:opacity-50"
      :disabled="submitting || parseFloat(amountStr) === 0"
      @click="handleAdd"
    >
      <template v-if="submitting">Сохранение...</template>
      <template v-else>Добавить</template>
    </button>

    <p v-if="error" class="text-error text-sm text-center">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { api } from '@/api/client'
import AppIcon from '@/components/ui/AppIcon.vue'

const props = defineProps<{ budgetId?: string }>()
const emit = defineEmits<{ close: []; added: [] }>()

const type = ref<'expense' | 'income'>('expense')
const amountStr = ref('0')
const selectedCategory = ref<any>(null)
const note = ref('')
const submitting = ref(false)
const error = ref('')
const categories = ref<any[]>([])

const keypadKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '0', 'backspace']

const displayAmount = computed(() => {
  if (amountStr.value === '0') return '0'
  return amountStr.value.replace('.', ',')
})

async function loadCategories() {
  if (!props.budgetId) return
  try {
    categories.value = await api(`/categories/?budget=${props.budgetId}`)
    if (categories.value.length > 0 && !selectedCategory.value) {
      selectedCategory.value = categories.value[0]
    }
  } catch {
    // ignore
  }
}

onMounted(loadCategories)
watch(() => props.budgetId, loadCategories)

function handleKey(key: string) {
  if (key === 'backspace') {
    amountStr.value = amountStr.value.length > 1 ? amountStr.value.slice(0, -1) : '0'
  } else if (key === ',') {
    if (!amountStr.value.includes('.')) {
      amountStr.value += '.'
    }
  } else {
    if (amountStr.value === '0') {
      amountStr.value = key
    } else {
      amountStr.value += key
    }
  }
}

async function handleAdd() {
  const amount = parseFloat(amountStr.value)
  if (amount <= 0) return
  if (!props.budgetId) {
    error.value = 'Бюджет не найден'
    return
  }

  submitting.value = true
  error.value = ''

  try {
    await api('/transactions/', {
      method: 'POST',
      body: JSON.stringify({
        budget: props.budgetId,
        category: selectedCategory.value?.id || null,
        amount: amountStr.value,
        type: type.value,
        note: note.value,
        occurred_at: new Date().toISOString(),
      }),
    })
    emit('added')
    emit('close')
  } catch (e: any) {
    error.value = e?.detail || e?.amount?.[0] || 'Ошибка при сохранении'
  } finally {
    submitting.value = false
  }
}
</script>
