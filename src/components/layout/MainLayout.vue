<template>
  <div class="min-h-screen bg-surface flex flex-col">
    <TopAppBar />
    <main class="flex-1 pb-24">
      <router-view />
    </main>
    <BottomNavBar @add-transaction="showAddTransaction = true" />

    <BottomSheet v-model:visible="showAddTransaction">
      <AddTransactionSheet @close="showAddTransaction = false" />
    </BottomSheet>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TopAppBar from '@/components/navigation/TopAppBar.vue'
import BottomNavBar from '@/components/navigation/BottomNavBar.vue'
import BottomSheet from '@/components/layout/BottomSheet.vue'
import AddTransactionSheet from '@/views/sheets/AddTransactionSheet.vue'

const showAddTransaction = ref(false)
</script>
