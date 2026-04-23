<template>
  <div class="flex flex-col gap-1">
    <label v-if="label" class="text-xs font-semibold tracking-[0.05em] text-on-surface-variant ml-4">
      {{ label }}
    </label>
    <div class="relative">
      <input
        v-model="model"
        :type="showPassword ? 'text' : type"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        class="w-full h-14 px-6 rounded-[20px] border border-outline-variant bg-surface-container-lowest text-on-surface text-sm placeholder:text-outline outline-none transition-all focus:ring-2 focus:ring-primary focus:border-primary disabled:opacity-50"
        :class="{ 'pr-12': type === 'password' }"
      />
      <button
        v-if="type === 'password'"
        type="button"
        class="absolute right-4 top-1/2 -translate-y-1/2 text-outline hover:text-primary transition-colors"
        @click="showPassword = !showPassword"
      >
        <span class="material-symbols-outlined text-xl">
          {{ showPassword ? 'visibility_off' : 'visibility' }}
        </span>
      </button>
    </div>
    <p v-if="error" class="text-xs text-error ml-4">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const model = defineModel<string>()
const showPassword = ref(false)

interface Props {
  label?: string
  type?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  error?: string
}

withDefaults(defineProps<Props>(), {
  label: '',
  type: 'text',
  placeholder: '',
  required: false,
  disabled: false,
  error: '',
})
</script>
