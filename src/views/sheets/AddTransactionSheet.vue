<template>
  <div class="flex flex-col gap-6">
    <!-- Segment Tabs -->
    <div class="flex p-1 bg-surface-container rounded-full w-full max-w-[280px] mx-auto">
      <button
        class="flex-1 py-2.5 rounded-full text-base font-medium shadow-sm transition-colors"
        :class="type === 'expense' ? 'bg-error-container text-on-error-container' : 'text-on-surface-variant'"
        @click="type = 'expense'"
      >
        Расход
      </button>
      <button
        class="flex-1 py-2.5 rounded-full text-base font-medium transition-colors"
        :class="type === 'income' ? 'bg-primary-fixed text-on-primary-fixed' : 'text-on-surface-variant'"
        @click="type = 'income'"
      >
        Доход
      </button>
    </div>

    <!-- Amount Display -->
    <div class="text-center py-2">
      <span class="text-[56px] leading-[64px] font-bold text-on-surface tracking-tighter">
        ₽ {{ displayAmount }}
      </span>
    </div>

    <!-- Category Grid -->
    <div class="grid grid-cols-4 gap-y-6 gap-x-2">
      <button
        v-for="cat in categories"
        :key="cat.name"
        class="flex flex-col items-center gap-1 group"
        @click="selectedCategory = cat.name"
      >
        <div
          class="w-[52px] h-[52px] rounded-[12px] flex items-center justify-center transition-transform group-active:scale-95"
          :class="selectedCategory === cat.name
            ? 'bg-primary-container text-on-primary-container'
            : 'bg-surface-container text-outline'"
        >
          <AppIcon :name="cat.icon" />
        </div>
        <span
          class="text-xs text-center"
          :class="selectedCategory === cat.name ? 'text-on-surface' : 'text-on-surface-variant'"
        >
          {{ cat.name }}
        </span>
      </button>
      <button class="flex flex-col items-center gap-1 group">
        <div class="w-[52px] h-[52px] rounded-[12px] border border-outline-variant bg-surface-container-lowest flex items-center justify-center group-active:scale-95 transition-transform">
          <AppIcon name="more_horiz" class="text-outline" />
        </div>
        <span class="text-xs text-on-surface-variant text-center">+ Ещё</span>
      </button>
    </div>

    <!-- Note & Date -->
    <div class="flex gap-2 items-center">
      <div class="flex-1 bg-surface-container-low border border-outline-variant rounded-[20px] px-4 py-3 flex items-center gap-2 focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all">
        <AppIcon name="edit" class="text-outline" :size="20" />
        <input
          v-model="note"
          type="text"
          placeholder="Комментарий..."
          class="bg-transparent border-none outline-none w-full text-sm text-on-surface placeholder:text-outline p-0 focus:ring-0"
        />
      </div>
      <button class="bg-surface-container rounded-full px-4 py-3 flex items-center gap-1 active:bg-surface-container-high transition-colors">
        <AppIcon name="schedule" class="text-on-surface-variant" :size="18" />
        <span class="text-base font-medium text-on-surface-variant whitespace-nowrap">Сегодня</span>
      </button>
    </div>

    <!-- Numeric Keypad -->
    <div class="grid grid-cols-3 gap-y-2 gap-x-2 px-4">
      <button
        v-for="key in keypadKeys"
        :key="key"
        class="h-14 text-2xl font-semibold text-on-surface rounded-[20px] active:bg-surface-container-high transition-colors flex items-center justify-center"
        @click="handleKey(key)"
      >
        <AppIcon v-if="key === 'backspace'" name="backspace" :size="28" class="text-on-surface" />
        <template v-else>{{ key }}</template>
      </button>
    </div>

    <!-- Add Button -->
    <button
      class="w-full bg-secondary-container text-on-secondary-container rounded-full py-4 text-base font-medium shadow-sm active:scale-[0.98] transition-transform flex items-center justify-center"
      @click="handleAdd"
    >
      Добавить
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppIcon from '@/components/ui/AppIcon.vue'

const emit = defineEmits<{ close: [] }>()

const type = ref<'expense' | 'income'>('expense')
const amountStr = ref('0')
const selectedCategory = ref('Продукты')
const note = ref('')

const categories = [
  { name: 'Продукты', icon: 'local_dining' },
  { name: 'Кафе', icon: 'coffee' },
  { name: 'Досуг', icon: 'attractions' },
  { name: 'Здоровье', icon: 'favorite' },
  { name: 'Интернет', icon: 'wifi' },
  { name: 'Свет', icon: 'lightbulb' },
  { name: 'Счета', icon: 'receipt_long' },
]

const keypadKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '0', 'backspace']

const displayAmount = computed(() => {
  if (amountStr.value === '0') return '0'
  return amountStr.value.replace('.', ',')
})

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

function handleAdd() {
  // TODO: save to Firestore
  emit('close')
}
</script>
