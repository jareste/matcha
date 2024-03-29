import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import { BootstrapVue3 } from 'bootstrap-vue-3'
import { createRouter, createWebHistory } from 'vue-router'
import LoginRegister from './components/LoginRegister.vue'
import UploadPhoto from './components/UploadPhoto.vue'

const routes = [
    { path: '/login-register', component: LoginRegister },
    { path: '/upload-photo', component: UploadPhoto }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)

app.use(BootstrapVue3)
app.use(router)
app.mount('#app')