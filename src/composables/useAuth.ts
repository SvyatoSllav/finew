import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api, setTokens, clearTokens } from '@/api/client'
import { useAuthStore } from '@/stores/auth'

export function useAuth() {
  const router = useRouter()
  const authStore = useAuthStore()
  const loading = ref(false)
  const error = ref('')

  async function login(email: string, password: string) {
    loading.value = true
    error.value = ''
    try {
      const data = await api('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      setTokens(data.tokens.access, data.tokens.refresh)
      authStore.setUser(data.user)
      await router.push('/dashboard')
    } catch (e: any) {
      error.value = e.detail || e.email?.[0] || 'Неверный email или пароль'
    } finally {
      loading.value = false
    }
  }

  async function signUp(email: string, password: string, displayName: string) {
    loading.value = true
    error.value = ''
    try {
      const data = await api('/auth/register/', {
        method: 'POST',
        body: JSON.stringify({ email, password, display_name: displayName }),
      })
      setTokens(data.tokens.access, data.tokens.refresh)
      authStore.setUser(data.user)
      await router.push('/dashboard')
    } catch (e: any) {
      error.value = e.detail || e.email?.[0] || e.password?.[0] || 'Ошибка при создании аккаунта'
    } finally {
      loading.value = false
    }
  }

  async function signInWithGoogle() {
    loading.value = true
    error.value = 'Google OAuth пока недоступен'
    loading.value = false
  }

  async function logout() {
    clearTokens()
    authStore.clearUser()
    await router.push('/welcome')
  }

  async function fetchMe() {
    try {
      const user = await api('/auth/me/')
      authStore.setUser(user)
      return user
    } catch {
      clearTokens()
      authStore.clearUser()
      return null
    }
  }

  return { login, signUp, signInWithGoogle, logout, fetchMe, loading, error }
}
