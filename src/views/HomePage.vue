<template>
  <div class="homepage">
    <!--TODO: Вынести хэдер в отдельной компонент лэйаута + авторизацию и регстрацию в отдельный компонент лэйаута-->
    <img alt="Логотип" src="@vue-icons/FineWFullLogo.svg"/>
    <div class="homepage__current-budget">
      <h2 class="homepage__current-budget__title">Выбранный счёт:</h2>
      <select v-model="selectedBudgetId" class="homepage__current-budget__select" @change="onBudgetChange">
        <option v-for="budget in allUserBudgets.value" :key="budget.id" :value="budget.id">
          {{ budget.name }}
        </option>
      </select>
    </div>
    <!--TODO: Вынести в отдельный компонент-->
    <div class="homepage__transaction-info">
      <div class="homepage__transaction-info__income">
        <h4 class="homepage__transaction-info__income__title">Доход</h4>
        <p class="homepage__transaction-info__income__amount"></p>
      </div>
      <div class="homepage__transaction-info__expenses">
        <h4 class="homepage__transaction-info__expenses__title">Затраты</h4>
        <p class="homepage__transaction-info__expenses__amount"></p>
      </div>
    </div>
    <!--    TODO: в отдельный компонент категорий-->
    <div class="homepage__categories">
      <div v-for="category in currentCategories.value" class="homepage__categories__category"
           @click="selectedCategoryId = category.id">
        <div class="homepage__categories__category__icon">
          <img :src="`/categoryIcons/${category.category_icon_name}.svg`" alt="Логотип"/>
        </div>
        <p class="homepage__categories__category__name">{{ category.category_name }}</p>
      </div>
    </div>
  </div>
  <button @click="logout">Logout</button>
  <button @click="copyBudgetId">Поделиться счётом</button>
  <input v-model="sharedBudgetId" placeholder="Введите ID счёта для поделения" type="text"/>
  <button @click="addBudget">Добавить счёт</button>
  <input v-model="transactionAmount" placeholder="Сумма транзакции" type="number"/>
  <button @click="addTransaction">Добавить транзакцию</button>
</template>

<script lang="ts" setup>
import {onMounted, ref, computed} from 'vue';
import {signOut} from 'firebase/auth';
import {useRouter} from 'vue-router';
import {getCurrentUser, useCollection, useFirebaseAuth, useFirestore, useDocument} from "vuefire";
import {collection, query, where, updateDoc, doc} from "firebase/firestore";
import {useBudgetStore} from "@/stores/budget.ts";

const auth = useFirebaseAuth()
const db = useFirestore();
const router = useRouter();
const user = ref(<Object>{})
const currentBudget = ref(null);
const budgetStore = useBudgetStore();
const allUserBudgets = ref([]);
const selectedBudgetId = ref('');
const sharedBudgetId = ref('');
const transactionAmount = ref(0);
const selectedCategoryId = ref('');
const currentCategories = computed(() => {
  return useCollection(query(collection(db, 'categories'), where('budget_id', '==', budgetStore.currentBudgetId)));
})

const onBudgetChange = () => {
  budgetStore.setCurrentBudgetId(selectedBudgetId.value);
};

// Получаем все связанные бюджеты текущего пользователя
const getAllUserBudgets = () => {
  const allBudgetQuery = query(
      collection(db, 'Budgets'),
      where('shared_with', 'array-contains', user.value.uid)
  );
  const allBudgets = useCollection(allBudgetQuery);
  allBudgets.promise.value.then(() => {
    allUserBudgets.value = allBudgets;
  })
}

// Получаем бюджет текущего пользователя
const getCurrentBudget = () => {
  const currentBudgetQuery = query(
      collection(db, 'Budgets'),
      where('author_id', '==', user.value.uid)
  );
  const currentBudgetCollection = useCollection(currentBudgetQuery);
  currentBudgetCollection.promise.value.then(() => {
    currentBudget.value = currentBudgetCollection.value[0]; // Save the first budget
    budgetStore.setCurrentBudgetId(currentBudgetCollection.value[0].id); // Save the ID to the store
    selectedBudgetId.value = budgetStore.currentBudgetId;
  })
}

getCurrentUser().then((result) => {
  user.value = result;
  getAllUserBudgets();
  getCurrentBudget();
})

const copyBudgetId = () => {
  navigator.clipboard.writeText(budgetStore.currentBudgetId);
}

async function addBudget() {
  // OIMhDTjYU42tFerQAxMH
  const newBudgetDoc = doc(collection(db, 'Budgets'), sharedBudgetId.value)
  const newBudget = useDocument(newBudgetDoc)
  newBudget.promise.value.then(() => {
    newBudget.value.shared_with.push(user.value.uid);
    updateDoc(newBudgetDoc, {...newBudget.value});
  })
}

const addTransaction = async () => {
  const categoryDoc = doc(collection(db, 'categories'), selectedCategoryId.value)
  const category = useDocument(categoryDoc)
  category.promise.value.then(() => {
    category.value.purchases.push({
      created_at: new Date(),
      amount: transactionAmount.value,
    })
    updateDoc(categoryDoc, {...category.value});
  })
}


onMounted(() => {
  auth.onAuthStateChanged((currentUser) => {
    user.value = currentUser;
  });
});

const logout = async () => {
  try {
    await signOut(auth);
    await router.push('/login');
  } catch (error) {
    console.error('Error logging out:', error);
  }
};
</script>

<style lang="scss" scoped>
.homepage {
  padding: 24px;
}
</style>