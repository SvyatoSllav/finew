import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/LoginPage.vue';
import SignUpPage from '@/views/SignUpPage.vue';
import {useFirebaseAuth} from "vuefire";


const routes = [
    { path: '/', component: HomePage, meta: { requiresAuth: true } },
    { path: '/login', component: LoginPage },
    { path: '/signup', component: SignUpPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
    const auth = useFirebaseAuth()
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    const isAuthenticated = auth.currentUser;

    if (requiresAuth && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router;