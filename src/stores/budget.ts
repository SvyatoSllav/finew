import {defineStore} from 'pinia'

export const useBudgetStore = defineStore('Budget', {
    state: () => ({
        currentBudgetId: null,
    }),
    actions: {
        setCurrentBudgetId(budgetId) {
            this.currentBudgetId = budgetId;
        },
    },
    getters: {},
})