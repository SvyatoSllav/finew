import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { isAuthenticated } from '@/api/client'

const routes: RouteRecordRaw[] = [
  {
    path: '/welcome',
    name: 'welcome',
    component: () => import('@/views/auth/WelcomePage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/auth/SignUpPage.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/',
    component: () => import('@/components/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/main/DashboardPage.vue') },
      { path: 'transactions', name: 'transactions', component: () => import('@/views/main/TransactionHistoryPage.vue') },
      { path: 'analytics', name: 'analytics', component: () => import('@/views/main/AnalyticsPage.vue') },
      { path: 'profile', name: 'profile', component: () => import('@/views/main/ProfilePage.vue') },
    ],
  },
  {
    path: '/transactions/:id',
    name: 'transaction-detail',
    component: () => import('@/views/sub/TransactionDetailPage.vue'),
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/budget/:id/settings',
    name: 'budget-settings',
    component: () => import('@/views/sub/BudgetSettingsPage.vue'),
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/welcome',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const authed = isAuthenticated()

  if (to.meta.requiresAuth && !authed) {
    return { name: 'welcome' }
  }

  if (to.meta.requiresGuest && authed) {
    return { name: 'dashboard' }
  }
})

export default router
