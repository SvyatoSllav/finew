<template>
  <div class="flex flex-col gap-8">
    <!-- Header -->
    <div class="flex justify-between items-start pt-2">
      <div class="flex flex-col gap-1">
        <h1 class="text-2xl font-semibold text-on-surface">Пригласить в бюджет</h1>
        <p class="text-sm text-outline">Основной</p>
      </div>
      <button
        class="w-8 h-8 flex items-center justify-center rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container transition-colors"
        @click="$emit('close')"
      >
        <AppIcon name="close" :size="20" />
      </button>
    </div>

    <!-- Invite Link -->
    <div class="bg-surface-container-low rounded-[24px] p-4 flex flex-col gap-4 border border-outline-variant/30">
      <div class="w-full bg-surface-container-lowest rounded-xl py-2 px-4 flex items-center shadow-sm">
        <span class="text-base text-on-surface truncate flex-1 select-all">finew.app/invite/{{ inviteCode }}</span>
      </div>
      <div class="flex gap-2 w-full">
        <button
          class="flex-1 flex items-center justify-center gap-1 py-2.5 rounded-xl border border-outline-variant text-primary hover:bg-surface-container transition-colors active:scale-[0.98]"
          @click="copyLink"
        >
          <AppIcon name="content_copy" :size="20" />
          <span class="text-base font-medium">Копировать</span>
        </button>
        <button class="flex-1 flex items-center justify-center gap-1 py-2.5 rounded-xl border border-outline-variant text-primary hover:bg-surface-container transition-colors active:scale-[0.98]">
          <AppIcon name="ios_share" :size="20" />
          <span class="text-base font-medium">Поделиться</span>
        </button>
      </div>
    </div>

    <!-- Role Selector -->
    <div class="flex flex-col gap-2">
      <span class="text-xs font-semibold tracking-[0.05em] text-outline uppercase pl-2">Роль</span>

      <label class="relative flex items-center p-4 rounded-[20px] border-2 cursor-pointer transition-all"
        :class="selectedRole === 'editor' ? 'border-primary bg-surface-container-lowest' : 'border-outline-variant/60 bg-surface-container-lowest'"
      >
        <input type="radio" name="role" value="editor" v-model="selectedRole" class="sr-only" />
        <div class="flex items-center gap-4 flex-1">
          <div class="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center text-on-primary-fixed shrink-0">
            <AppIcon name="edit_square" :fill="1" />
          </div>
          <div class="flex flex-col">
            <span class="text-base font-medium text-on-surface">Редактор</span>
            <span class="text-xs text-outline">Может добавлять и изменять операции</span>
          </div>
        </div>
        <div v-if="selectedRole === 'editor'" class="w-6 h-6 rounded-full bg-primary text-surface-container-lowest flex items-center justify-center shrink-0 ml-4 shadow-sm">
          <AppIcon name="check" :size="16" :weight="600" />
        </div>
        <div v-else class="w-6 h-6 rounded-full border-2 border-outline-variant/50 shrink-0 ml-4"></div>
      </label>

      <label class="relative flex items-center p-4 rounded-[20px] border cursor-pointer transition-all hover:border-outline-variant hover:bg-surface-container-low"
        :class="selectedRole === 'viewer' ? 'border-primary bg-surface-container-lowest' : 'border-outline-variant/60 bg-surface-container-lowest'"
      >
        <input type="radio" name="role" value="viewer" v-model="selectedRole" class="sr-only" />
        <div class="flex items-center gap-4 flex-1">
          <div class="w-12 h-12 rounded-full bg-surface-container-high flex items-center justify-center text-on-surface-variant shrink-0">
            <AppIcon name="visibility" />
          </div>
          <div class="flex flex-col">
            <span class="text-base text-on-surface">Наблюдатель</span>
            <span class="text-xs text-outline">Только просмотр операций</span>
          </div>
        </div>
        <div v-if="selectedRole === 'viewer'" class="w-6 h-6 rounded-full bg-primary text-surface-container-lowest flex items-center justify-center shrink-0 ml-4 shadow-sm">
          <AppIcon name="check" :size="16" :weight="600" />
        </div>
        <div v-else class="w-6 h-6 rounded-full border-2 border-outline-variant/50 shrink-0 ml-4"></div>
      </label>
    </div>

    <!-- Footer -->
    <div class="flex flex-col gap-4 items-center mt-2">
      <span class="text-xs text-outline flex items-center gap-1">
        <AppIcon name="schedule" :size="14" />
        Ссылка действительна 7 дней
      </span>
      <button class="w-full py-4 bg-secondary-container text-surface-container-lowest rounded-full text-base font-medium shadow-md hover:opacity-95 active:scale-[0.98] transition-all flex items-center justify-center gap-2">
        <AppIcon name="person_add" :size="20" />
        Создать приглашение
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppIcon from '@/components/ui/AppIcon.vue'

defineEmits<{ close: [] }>()

const selectedRole = ref('editor')
const inviteCode = ref('Abc123')

function copyLink() {
  navigator.clipboard.writeText(`finew.app/invite/${inviteCode.value}`)
}
</script>
