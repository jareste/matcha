<template>
  <div>
    <nav>
      <div class="links">
        <router-link to="/login-register">Login/Register</router-link> |
        <router-link to="/upload-photo">Upload Photo</router-link> |
        <router-link to="/profile">Profile Page</router-link> |
        <router-link to="/match">Match</router-link>
      </div>
      <div class="user-info" v-if="user.username && user.photoUrl">
        <img :src="user.photoUrl" alt="User photo" class="user-photo">
        <router-link to="/profile" class="username">{{ user.username }}</router-link>
      </div>
    </nav>
    <router-view></router-view>
    <ChatComponent v-if="user.isProfileLoaded" />
  </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';
import ChatComponent from './components/ChatComponent.vue';

export default {
  components: {
    ChatComponent
  },
  data() {
    return {
      isChatOpen: false,
      // user: {
      //   username: '',
      //   photoUrl: ''
      // }
    }
  },
  methods: {
    toggleChat() {
      this.isChatOpen = !this.isChatOpen;
    }
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('http://localhost:5000/getProfile')
      .then(response => {
          this.user.username = response.data.username;
          this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
          this.user.isProfileLoaded = true;
        })
      .catch(error => {
        console.log(error);
      });
    }
  },
  setup () {
    const user = inject('user');
    // let isProfileLoaded = inject('isProfileLoaded');
    return { user };
  }
  
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
}

.links {
  flex-grow: 1;
}

.user-info {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.user-photo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

@media (max-width: 600px) {
  .user-photo {
    width: 30px;
    height: 30px;
  }
}
</style>