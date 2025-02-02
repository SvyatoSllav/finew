<template>
    <div>
        <h1>Welcome to FinControl</h1>
        <button @click="logout">Logout</button>
        <div v-if="user">
            <p>Logged in as: {{ user.email }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';
import {useFirebaseAuth} from "vuefire";

const auth = useFirebaseAuth()
const user = ref(auth.currentUser);
const router = useRouter();

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