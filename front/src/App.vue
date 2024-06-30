<template>
  <div>
    <nav>
      <div class="nav-content">
        <div class="links">
          <router-link to="/login-register">Login/Register</router-link> |
          <router-link to="/profile">Profile Page</router-link> |
          <router-link to="/match">Match</router-link>
        </div>
        <div class="user-info" v-if="user.username && user.photoUrl">
          <div class="search-bar">
            <input v-model="searchQuery" @keyup.enter="searchProfile" placeholder="Search for user">
            <button @click="searchProfile">Search</button>
          </div>
        </div>
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
      searchQuery: ''
    }
  },
  methods: {
    toggleChat() {
      this.isChatOpen = !this.isChatOpen;
    },
    searchProfile() {
      if (this.searchQuery) {
        this.$router.push(`/profile/${this.searchQuery}`);
      }
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
    return { user };
  }
}
</script>

<style scoped>
nav {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.nav-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.links {
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 10px;
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.user-photo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

@media (min-width: 600px) {
  nav {
    flex-direction: row;
  }
  
  .nav-content {
    flex-direction: row;
    justify-content: space-between;
    width: auto;
  }

  .links {
    margin-bottom: 0;
    margin-right: 20px;
  }

  .search-bar {
    margin-bottom: 0;
  }

  .user-info {
    margin-top: 0;
    margin-right: 20px;
  }
}

@media (max-width: 600px) {
  .user-photo {
    width: 30px;
    height: 30px;
  }
}
</style>
