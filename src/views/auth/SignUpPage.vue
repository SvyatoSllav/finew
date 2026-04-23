<template>
  <AuthLayout variant="card" :compact="true">
    <template #header>
      <div class="flex flex-col items-center text-white">
        <div class="mb-4 opacity-20">
          <AppIcon name="account_balance_wallet" :size="64" />
        </div>
        <h1 class="text-2xl font-semibold text-center">Присоединяйтесь к FineW</h1>
        <p class="text-sm text-white/80 text-center mt-1">Ваш совместный путь к финансовому спокойствию</p>
      </div>
    </template>

    <h2 class="text-lg font-semibold text-on-surface mb-6">Регистрация</h2>

    <form class="space-y-4" @submit.prevent="handleSignUp">
      <AppInput
        v-model="displayName"
        label="Имя"
        placeholder="Как вас зовут?"
        required
      />
      <AppInput
        v-model="email"
        label="Почта"
        placeholder="Введите вашу почту"
        type="email"
        required
      />
      <AppInput
        v-model="password"
        label="Пароль"
        placeholder="Придумайте пароль"
        type="password"
        required
      />

      <AppButton variant="filled" type="submit" :disabled="loading" class="mt-6">
        {{ loading ? 'Создание...' : 'Создать аккаунт' }}
      </AppButton>
    </form>

    <p v-if="error" class="text-sm text-error text-center mt-2">{{ error }}</p>

    <AppDivider />

    <AppButton variant="google" @click="handleGoogle">
      <img
        src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
        alt="Google"
        class="w-5 h-5"
      />
      Зарегистрироваться через Google
    </AppButton>

    <div class="mt-auto pt-8">
      <p class="text-sm text-center" style="color: #8E8E8E">
        Уже есть аккаунт?
        <router-link to="/login" class="font-semibold" style="color: #2B7979">Войти</router-link>
      </p>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppDivider from '@/components/ui/AppDivider.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import { useAuth } from '@/composables/useAuth'

const displayName = ref('')
const email = ref('')
const password = ref('')
const { signUp, signInWithGoogle, loading, error } = useAuth()

async function handleSignUp() {
  await signUp(email.value, password.value, displayName.value)
}

async function handleGoogle() {
  await signInWithGoogle()
}
</script>
