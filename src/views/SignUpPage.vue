<template>
    <h1>Sign Up</h1>
    <form @submit.prevent="signUp">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Sign Up</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
    <p @click="signInWithGoogle">Or, sign up with Google:</p>
    <button @click="createBudget">Create Budget</button>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import {GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { useRouter } from 'vue-router';
import {useFirebaseAuth, useFirestore, useCollection} from "vuefire";
import { collection, addDoc } from 'firebase/firestore';

const email = ref('');
const auth = useFirebaseAuth()
const db = useFirestore();
const password = ref('');
const router = useRouter();

const categoriesToCreate = [
    {
        category_name: 'Продукты',
        currency: 'RUB',
        purchases: [],
    },
]

const signUp = async () => {
    try {
        await createUserWithEmailAndPassword(auth, email.value, password.value).then((result) => {
            addDoc(collection(db, 'Budgets'), {
                author_id: result.user.uid,
                name: 'Основной',
                shared_with: [result.user.uid],
            }).then((result) => {
                categoriesToCreate.forEach(category => {
                    addDoc(collection(db, 'categories'), {
                        budget_id: result.id,
                        category_name: category.category_name,
                        currency: category.currency,
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