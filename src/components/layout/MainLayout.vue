<template>
  <div class="min-h-screen bg-surface flex flex-col">
    <TopAppBar />
    <main class="flex-1 pb-24">
      <router-view :key="refreshKey" />
    </main>
    <BottomNavBar @add-transaction="showAddTransaction = true" />

    <BottomSheet v-model:visible="showAddTransaction">
      <AddTransactionSheet
        :budget-id="budgetId"
        @close="showAddTransaction = false"
        @added="onTransactionAdded"
      />
    </BottomSheet>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/api/client'
import TopAppBar from '@/components/navigation/TopAppBar.vue'
import BottomNavBar from '@/components/navigation/BottomNavBar.vue'
import BottomSheet from '@/components/layout/BottomSheet.vue'
import AddTransactionSheet from '@/views/sheets/AddTransactionSheet.vue'

const showAddTransaction = ref(false)
const budgetId = ref<string>('')
const refreshKey = ref(0)

onMounted(async () => {
  try {
    const budgets = await api('/budgets/')
    if (budgets.length > 0) {
      budgetId.value = budgets[0].id
    }
  } catch {
    // ignore
  }
})

function onTransactionAdded() {
  refreshKey.value++
}
</script>
