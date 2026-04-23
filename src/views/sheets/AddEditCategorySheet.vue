<template>
  <div class="flex flex-col gap-6">
    <!-- Header -->
    <header class="flex justify-between items-center">
      <h1 class="text-2xl font-semibold text-on-surface">Новая категория</h1>
      <button
        class="w-8 h-8 flex items-center justify-center rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container transition-colors"
        @click="$emit('close')"
      >
        <AppIcon name="close" :size="20" />
      </button>
    </header>

    <!-- Type Selector -->
    <div class="bg-surface-container p-1 rounded-full flex">
      <button
        class="flex-1 py-2.5 rounded-full text-base font-medium text-center transition-all"
        :class="type === 'expense' ? 'bg-surface-container-lowest shadow-[0_2px_4px_rgba(0,0,0,0.04)] text-on-surface' : 'text-on-surface-variant'"
        @click="type = 'expense'"
      >
        Расход
      </button>
      <button
        class="flex-1 py-2.5 rounded-full text-base font-medium text-center transition-all"
        :class="type === 'income' ? 'bg-surface-container-lowest shadow-[0_2px_4px_rgba(0,0,0,0.04)] text-on-surface' : 'text-on-surface-variant'"
        @click="type = 'income'"
      >
        Доход
      </button>
    </div>

    <!-- Name Input -->
    <AppInput v-model="categoryName" label="Название" placeholder="Например, Транспорт" />

    <!-- Icon Picker -->
    <div>
      <label class="text-xs text-on-surface-variant mb-2 block ml-4">Иконка</label>
      <div class="grid grid-cols-5 gap-2 p-4 bg-surface-container-low rounded-[24px]">
        <button
          v-for="icon in availableIcons"
          :key="icon"
          class="aspect-square rounded-[16px] flex items-center justify-center transition-transform active:scale-95"
          :class="selectedIcon === icon
            ? 'bg-primary text-on-primary shadow-sm'
            : 'bg-surface-container-lowest text-on-surface-variant hover:bg-surface-container'"
          @click="selectedIcon = icon"
        >
          <AppIcon :name="icon" :fill="selectedIcon === icon ? 1 : 0" />
        </button>
      </div>
    </div>

    <!-- Color Picker -->
    <div>
      <label class="text-xs text-on-surface-variant mb-2 block ml-4">Цвет</label>
      <div class="flex gap-4 overflow-x-auto hide-scrollbar pb-2 px-2">
        <button
          v-for="color in availableColors"
          :key="color"
          class="w-12 h-12 shrink-0 rounded-full flex items-center justify-center border-2 border-surface-container-lowest outline-none transition-transform hover:scale-105"
          :class="{ 'ring-2 ring-offset-1': selectedColor === color }"
          :style="{ backgroundColor: color, ringColor: color }"
          @click="selectedColor = color"
        >
          <AppIcon v-if="selectedColor === color" name="check" class="text-white font-bold" />
        </button>
      </div>
    </div>

    <!-- Save Button -->
    <button
      class="w-full h-14 rounded-[20px] bg-secondary-container text-on-secondary-container text-base font-medium flex items-center justify-center hover:opacity-90 active:scale-[0.98] transition-all"
      @click="handleSave"
    >
      Сохранить
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import AppInput from '@/components/ui/AppInput.vue'

const emit = defineEmits<{ close: [] }>()

const type = ref<'expense' | 'income'>('expense')
const categoryName = ref('')
const selectedIcon = ref('directions_car')
const selectedColor = ref('#ff793d')

const availableIcons = [
  'directions_car', 'restaurant', 'shopping_cart', 'home', 'flight',
  'local_cafe', 'pets', 'health_and_safety', 'checkroom', 'more_horiz',
]

const availableColors = [
  '#ff793d', '#53621d', '#0f6667', '#ba1a1a',
  '#6c7b33', '#338080', '#a53c00', '#56641f',
]

function handleSave() {
  // TODO: save to Firestore
  emit('close')
}
</script>
