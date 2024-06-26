import { createApp, reactive } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import { BootstrapVue3, BFooter } from 'bootstrap-vue-3'
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import axios from 'axios'

async function initializeApp() {
    if (localStorage.getItem('token')) {
        try {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token');        
            const response = await axios.get('http://localhost:5000/getProfile');
            console.log(response.data);
            if (response.data.username) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token');
            } else {
                localStorage.removeItem('token');
            }
        } catch (error) {
            localStorage.removeItem('token');
        }
    }

    const router = createRouter({
        history: createWebHistory(),
        routes
    })

    const app = createApp(App)

    const user = reactive({
        username: '',
        photoUrl: '',
    });
    app.provide('user', user);

    app.use(BootstrapVue3)
    app.component('BFooter', BFooter)

    app.use(router)
    app.mount('#app')
}

initializeApp()
