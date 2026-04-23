<template>
  <AuthLayout variant="fullscreen">
    <div class="flex flex-col items-center justify-between min-h-screen text-white relative overflow-hidden">
      <!-- Decorative blurs -->
      <div class="absolute top-0 left-0 w-full h-1/2 opacity-20 pointer-events-none overflow-hidden">
        <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-white blur-3xl"></div>
        <div class="absolute top-1/4 -right-24 w-64 h-64 rounded-full bg-cta blur-3xl"></div>
      </div>

      <!-- Logo & Tagline -->
      <main class="relative z-10 flex flex-col items-center justify-center flex-grow px-6 w-full">
        <div class="flex flex-col items-center text-center space-y-4">
          <div class="relative">
            <h1 class="text-7xl font-black tracking-tighter">FineW</h1>
            <div class="absolute -right-2 -bottom-2 w-8 h-8 bg-cta rounded-full border-4 flex items-center justify-center" style="border-color: #7D8D43">
              <AppIcon name="favorite" :size="16" :fill="1" />
            </div>
          </div>
          <p class="text-lg opacity-90">Финансы для двоих</p>
        </div>

        <!-- Decorative illustration -->
        <div class="mt-8 w-full flex justify-center items-center h-48 relative">
          <div class="absolute w-32 h-32 bg-white/10 rounded-[40px] rotate-12"></div>
          <div class="absolute w-32 h-32 bg-white/5 rounded-[40px] -rotate-6"></div>
          <div class="z-20 flex -space-x-4">
            <div class="w-20 h-20 rounded-full border-4 border-white overflow-hidden shadow-lg bg-surface-container-high flex items-center justify-center">
              <AppIcon name="person" :size="32" class="text-outline" />
            </div>
            <div class="w-20 h-20 rounded-full border-4 border-white overflow-hidden shadow-lg bg-surface-container-high translate-y-4 flex items-center justify-center">
              <AppIcon name="person" :size="32" class="text-outline" />
            </div>
          </div>
        </div>
      </main>

      <!-- Bottom Actions -->
      <footer class="relative z-10 w-full px-6 pb-8 space-y-4">
        <AppButton variant="filled" @click="$router.push('/signup')">
          Создать аккаунт
        </AppButton>
        <AppButton variant="outlined" @click="$router.push('/login')">
          Войти
        </AppButton>
        <div class="text-center pt-4 px-4">
          <p class="text-xs text-white/70 leading-tight">
            Продолжая, вы соглашаетесь с
            <a href="#" class="underline underline-offset-2 text-white">условиями использования</a>
            и
            <a href="#" class="underline underline-offset-2 text-white">политикой конфиденциальности</a>
          </p>
        </div>
        <div class="h-2"></div>
      </footer>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import AuthLayout from '@/components/layout/AuthLayout.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
</script>
