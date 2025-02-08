<template>
  <h1>Sign Up</h1>
  <form @submit.prevent="signUp">
    <input v-model="email" placeholder="Email" required type="email"/>
    <input v-model="password" placeholder="Password" required type="password"/>
    <button type="submit">Sign Up</button>
  </form>
  <p>Already have an account?
    <router-link to="/login">Login</router-link>
  </p>
  <p @click="signInWithGoogle">Or, sign up with Google:</p>
  <button @click="createBudget">Create Budget</button>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import {createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup} from 'firebase/auth';
import {useRouter} from 'vue-router';
import {useFirebaseAuth, useFirestore} from "vuefire";
import {addDoc, collection} from 'firebase/firestore';
import {categoriesToCreate} from '@/utils/consts.js'
import {useBudgetStore} from "@/stores/budget.ts";

const email = ref('');
const auth = useFirebaseAuth()
const db = useFirestore();
const password = ref('');
const router = useRouter();
const budgetStore = useBudgetStore();

const signUp = async () => {
  try {
    await createUserWithEmailAndPassword(auth, email.value, password.value).then((result) => {
      addDoc(collection(db, 'Budgets'), {
        author_id: result.user.uid,
        name: 'Основной',
        shared_with: [result.user.uid],
        currency: 'RUB',
      }).then((result) => {
        budgetStore.setCurrentBudgetId(result.id);
        categoriesToCreate.forEach(category => {
          addDoc(collection(db, 'categories'), {
            budget_id: result.id,
            category_name: category.category_name,
            category_icon_name: category.iconName,
            purchases: [],
          });
        });
        router.push('/');
      })
    });
  } catch (error) {
    console.error('Error signing up:', error);
    alert('Error creating account');
  }
};
const signInWithGoogle = async () => {
  try {
    const provider = new GoogleAuthProvider();
    await signInWithPopup(auth, provider).then((result) => {
      console.log('Successfully signed in with Google:', result.user);
      router.push('/');
    }).catch((error) => {
      console.error('Error signing up:', error);
      alert('Error creating account');
    });
  } catch (error) {
    console.error('Error signing up:', error);
    alert('Error creating account');
  }
}
</script>