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
import {useCurrentUser, useFirebaseAuth, useFirestore} from "vuefire";
import {collection, query, getDocs} from "firebase/firestore";

const auth = useFirebaseAuth()
const db = useFirestore();
const user = useCurrentUser();
const router = useRouter();
// const budgets = query(collection(db, 'budgets')).where('shared_with', 'array-contains', user.value?.uid);
// const budgetsIds = budgets.value.map((doc) => doc.id);
// const categories = query(collection(db, 'categories')).where('budget_id', 'in', budgetsIds);
//
//
//
// const q = query(collection(db, 'budgets')).where('shared_with', 'array-contains', user.value?.uid);
// const unsubscribe = onSnapshot(q, (querySnapshot) => {
//     const cities = [];
//     querySnapshot.forEach((doc) => {
//         cities.push(doc.data().name);
//     });
//     const budgetsIds = budgets.value.map((doc) => doc.id);
//     const categories = query(collection(db, 'categories')).where('budget_id', 'in', budgetsIds);
//     console.log("Current cities in CA: ", cities.join(", "));
// });



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