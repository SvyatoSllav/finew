import { createApp } from 'vue'
import { VueFire, VueFireAuth } from 'vuefire'
import router from './router';
import {firebaseApp} from './firebase'
import './style.scss'
import App from './App.vue'

const app = createApp(App)
app.use(router);
app.use(VueFire, {
    // imported above but could also just be created here
    firebaseApp,
    modules: [
        // we will see other modules later on
        VueFireAuth(),
    ],
})
app.mount('#app')
