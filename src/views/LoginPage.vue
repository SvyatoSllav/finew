<template>
    <div>
        <h1>Login</h1>
        <form @submit.prevent="login">
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useRouter } from 'vue-router';
import {useFirebaseAuth} from "vuefire";

const auth = useFirebaseAuth()
const email = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
    try {
        await signInWithEmailAndPassword(auth, email.value, password.value);
        await router.push('/');
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Invalid email or password');
    }
};
</script>