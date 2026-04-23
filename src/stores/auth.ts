import { defineStore } from 'pinia'
import { ref } from 'vue'

interface AuthUser {
  uid: string
  email: string
  display_name: string
  avatar_url?: string
  default_budget?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(null)

  function setUser(u: AuthUser) {
    user.value = u
  }

  function clearUser() {
    user.value = null
  }

  return { user, setUser, clearUser }
})
