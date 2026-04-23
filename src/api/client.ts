const BASE_URL = '/api'

function getTokens() {
  const access = localStorage.getItem('access_token')
  const refresh = localStorage.getItem('refresh_token')
  return { access, refresh }
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

export function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem('access_token')
}

async function refreshAccessToken(): Promise<string | null> {
  const { refresh } = getTokens()
  if (!refresh) return null

  const res = await fetch(`${BASE_URL}/auth/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })

  if (!res.ok) {
    clearTokens()
    return null
  }

  const data = await res.json()
  setTokens(data.access, data.refresh ?? refresh)
  return data.access
}

export async function api(path: string, options: RequestInit = {}): Promise<any> {
  const { access } = getTokens()

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  }

  if (access) {
    headers['Authorization'] = `Bearer ${access}`
  }

  let res = await fetch(`${BASE_URL}${path}`, { ...options, headers })

  // Try refreshing token on 401
  if (res.status === 401 && access) {
    const newAccess = await refreshAccessToken()
    if (newAccess) {
      headers['Authorization'] = `Bearer ${newAccess}`
      res = await fetch(`${BASE_URL}${path}`, { ...options, headers })
    }
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }))
    throw error
  }

  if (res.status === 204) return null
  return res.json()
}
