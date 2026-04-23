<template>
  <AuthLayout variant="card">
    <h2 class="text-lg font-semibold text-on-surface mb-8">Вход</h2>

    <form class="w-full flex flex-col gap-4" @submit.prevent="handleLogin">
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
        placeholder="Введите ваш пароль"
        type="password"
        required
      />

      <div class="flex justify-end -mt-1">
        <a href="#" class="text-sm font-medium" style="color: #2B7979">Забыли пароль?</a>
      </div>

      <AppButton variant="filled" type="submit" :disabled="loading" class="mt-4">
        {{ loading ? 'Загрузка...' : 'Войти' }}
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
      Войти через Google
    </AppButton>

    <div class="mt-auto pt-8">
      <p class="text-sm text-center" style="color: #8E8E8E">
        Нет аккаунта?
        <router-link to="/signup" class="font-semibold" style="color: #2B7979">Зарегистрируйтесь</router-link>
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
import { useAuth } from '@/composables/useAuth'

const email = ref('')
const password = ref('')
const { login, signInWithGoogle, loading, error } = useAuth()

async function handleLogin() {
  await login(email.value, password.value)
}

async function handleGoogle() {
  await signInWithGoogle()
}
</script>
