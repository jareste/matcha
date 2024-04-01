import LoginRegister from './components/LoginRegister.vue'
import UploadPhoto from './components/UploadPhoto.vue'
import ProfilePage from './components/ProfilePage.vue'

function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token != null;
}

const routes = [
    { 
        path: '/login-register', 
        component: LoginRegister,
        beforeEnter: (to, from, next) => {
            if (!isAuthenticated()) {
                next();
            } else {
                next('/profile');
            }
        }
    },
    { 
        path: '/upload-photo', 
        component: UploadPhoto,
        beforeEnter: (to, from, next) => {
            if (isAuthenticated()) {
                next();
            } else {
                next('/login-register');
            }
        }
    },
    { 
        path: '/profile', 
        component: ProfilePage,
        beforeEnter: (to, from, next) => {
            if (isAuthenticated()) {
                next();
            } else {
                next('/login-register');
            }
        }
    }
]

export default routes;