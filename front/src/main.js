import axios from 'axios'
import { createApp, reactive } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import { BootstrapVue3 } from 'bootstrap-vue-3'
import { createRouter, createWebHistory } from 'vue-router'
import LoginRegister from './components/LoginRegister.vue'
import UploadPhoto from './components/UploadPhoto.vue'
import ProfilePage from './components/ProfilePage.vue'

if (localStorage.getItem('token')) {
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token');
}

const routes = [
    { path: '/login-register', component: LoginRegister },
    { path: '/upload-photo', component: UploadPhoto },
    { path: '/profile', component: ProfilePage }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)

const user = reactive({
    username: '',
    photoUrl: ''
});
app.provide('user', user);

app.use(BootstrapVue3)
app.use(router)
app.mount('#app')
