<template>
    <div>
        <h1>Sign Up</h1>
        <form @submit.prevent="signUp">
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Sign Up</button>
        </form>
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
        <p @click="signInWithGoogle">Or, sign up with Google:</p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import {GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { useRouter } from 'vue-router';
import {useFirebaseAuth} from "vuefire";

const email = ref('');
const auth = useFirebaseAuth()
const password = ref('');
const router = useRouter();

const signUp = async () => {
    try {
        await createUserWithEmailAndPassword(auth, email.value, password.value);
        await router.push('/');
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