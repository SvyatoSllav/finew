<template>
  <SubPageLayout title="Настройки бюджета">
    <div class="flex flex-col gap-8">
      <!-- General info -->
      <section class="flex flex-col gap-4">
        <h2 class="text-xs font-semibold tracking-[0.05em] text-on-surface-variant uppercase">Основная информация</h2>
        <div class="bg-surface-container-lowest rounded-[24px] p-6 shadow-[0_2px_12px_rgba(0,0,0,0.04)] flex flex-col gap-6 border border-surface-variant">
          <AppInput v-model="budgetName" label="Название" />
          <div class="flex flex-col gap-1">
            <label class="text-xs text-on-surface-variant px-2">Валюта</label>
            <div class="relative">
              <select class="appearance-none bg-surface-container-low border border-outline-variant rounded-[20px] pl-12 pr-10 py-3 text-base text-on-surface outline-none focus:border-primary focus:ring-1 focus:ring-primary w-full cursor-pointer">
                <option value="RUB" selected>RUB — Российский рубль</option>
                <option value="USD">USD — Доллар США</option>
                <option value="EUR">EUR — Евро</option>
              </select>
              <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-2xl">🇷🇺</div>
              <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none text-on-surface-variant">
                <AppIcon name="expand_more" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Members -->
      <section class="flex flex-col gap-4">
        <h2 class="text-xs font-semibold tracking-[0.05em] text-on-surface-variant uppercase">Участники</h2>
        <div class="bg-surface-container-lowest rounded-[24px] shadow-[0_2px_12px_rgba(0,0,0,0.04)] border border-surface-variant overflow-hidden">
          <div
            v-for="(member, i) in members"
            :key="member.name"
            class="flex items-center p-4 gap-4"
            :class="{ 'border-b border-surface-variant': i < members.length - 1 }"
          >
            <AppAvatar :name="member.name" size="md" border />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <h3 class="text-base font-medium text-on-surface truncate">{{ member.name }}</h3>
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] tracking-wide"
                  :class="roleBadgeClass(member.role)"
                >
                  {{ roleLabel(member.role) }}
                </span>
              </div>
              <p class="text-xs text-on-surface-variant truncate">{{ member.email }}</p>
            </div>
            <button v-if="member.role !== 'owner'" class="text-on-surface-variant hover:text-on-surface transition-colors p-2 rounded-full hover:bg-surface-variant">
              <AppIcon name="more_vert" :size="20" />
            </button>
          </div>
        </div>
        <button
          class="w-full flex items-center justify-center gap-2 py-3 px-6 rounded-full border border-tertiary text-tertiary text-base font-medium hover:bg-tertiary/5 active:bg-tertiary/10 transition-colors"
          @click="showInvite = true"
        >
          <AppIcon name="person_add" :size="20" />
          Пригласить участника
        </button>
      </section>

      <!-- Categories -->
      <section class="flex flex-col gap-4">
        <h2 class="text-xs font-semibold tracking-[0.05em] text-on-surface-variant uppercase">Категории</h2>
        <div class="bg-surface-container-lowest rounded-[24px] shadow-[0_2px_12px_rgba(0,0,0,0.04)] border border-surface-variant overflow-hidden">
          <div
            v-for="(cat, i) in categoriesList"
            :key="cat.name"
            class="flex items-center p-4 gap-4 hover:bg-surface-container-low transition-colors"
            :class="{ 'border-b border-surface-variant': i < categoriesList.length - 1 }"
          >
            <AppIcon name="drag_indicator" class="text-outline cursor-grab" />
            <div class="w-10 h-10 rounded-full flex items-center justify-center" :style="{ backgroundColor: cat.color + '33' }">
              <AppIcon :name="cat.icon" :class="'text-[' + cat.color + ']'" />
            </div>
            <div class="flex-1">
              <h3 class="text-base font-medium text-on-surface">{{ cat.name }}</h3>
              <p class="text-xs text-on-surface-variant">{{ cat.type === 'expense' ? 'Расход' : 'Доход' }}</p>
            </div>
            <button class="text-outline hover:text-on-surface transition-colors p-2">
              <AppIcon name="edit" :size="20" />
            </button>
          </div>
        </div>
        <button
          class="w-full flex items-center justify-center gap-2 py-3 px-6 rounded-full border border-tertiary text-tertiary text-base font-medium hover:bg-tertiary/5 transition-colors"
          @click="showAddCategory = true"
        >
          <AppIcon name="add_circle" :size="20" />
          Добавить категорию
        </button>
      </section>

      <!-- Danger zone -->
      <section class="mt-8 pt-8 border-t border-surface-variant">
        <button class="w-full flex items-center justify-center gap-2 py-4 px-6 rounded-full bg-error-container text-on-error-container text-base font-medium hover:opacity-90 active:scale-95 transition-all">
          <AppIcon name="delete" :size="20" />
          Удалить бюджет
        </button>
      </section>
    </div>

    <!-- Sheets -->
    <BottomSheet v-model:visible="showInvite">
      <InviteMemberSheet @close="showInvite = false" />
    </BottomSheet>
    <BottomSheet v-model:visible="showAddCategory">
      <AddEditCategorySheet @close="showAddCategory = false" />
    </BottomSheet>
  </SubPageLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SubPageLayout from '@/components/layout/SubPageLayout.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import BottomSheet from '@/components/layout/BottomSheet.vue'
import InviteMemberSheet from '@/views/sheets/InviteMemberSheet.vue'
import AddEditCategorySheet from '@/views/sheets/AddEditCategorySheet.vue'

defineProps<{ id: string }>()

const budgetName = ref('Основной')
const showInvite = ref(false)
const showAddCategory = ref(false)

const members = ref([
  { name: 'Алексей С.', email: 'alex@example.com', role: 'owner' },
  { name: 'Мария И.', email: 'maria@example.com', role: 'editor' },
])

const categoriesList = ref([
  { name: 'Продукты', icon: 'shopping_cart', color: '#a53c00', type: 'expense' },
  { name: 'Транспорт', icon: 'directions_car', color: '#0f6667', type: 'expense' },
  { name: 'Зарплата', icon: 'payments', color: '#53621d', type: 'income' },
])

function roleBadgeClass(role: string) {
  switch (role) {
    case 'owner': return 'bg-primary-container text-on-primary-container'
    case 'editor': return 'bg-tertiary-container text-on-tertiary-container'
    default: return 'bg-surface-variant text-on-surface-variant'
  }
}

function roleLabel(role: string) {
  switch (role) {
    case 'owner': return 'Владелец'
    case 'editor': return 'Редактор'
    default: return 'Наблюдатель'
  }
}
</script>
