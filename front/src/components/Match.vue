<template>
  <div>
    <h1>Find Your Match</h1>
    <div v-if="users.length">
      <div v-for="user in users" :key="user.id" class="user-card">
        <img :src="user.photo" alt="User photo" class="user-photo" />
        <p>{{ user.username }}</p>
        <button @click="likeUser(user.id)">Like</button>
        <button @click="passUser(user.id)">Pass</button>
      </div>
    </div>
    <h2>Your Matches</h2>
    <div v-if="matches.length">
      <div v-for="match in matches" :key="match.id" class="match-card">
        <img :src="match.photo" alt="Match photo" class="match-photo" />
        <p>{{ match.username }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      matches: [],
      user: {
        id: 1,
      },
    };
  },
  methods: {
    fetchUsers() {
      axios.get('http://localhost:5000/users')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchMatches() {
      axios.get(`http://localhost:5000/matches/${this.user.id}`)
        .then(response => {
          this.matches = response.data.matches;
        })
        .catch(error => {
          console.error(error);
        });
    },
    likeUser(likedUserId) {
      axios.post('http://localhost:5000/like', {
        user_id: this.user.id,
        liked_user_id: likedUserId,
      })
      .then(response => {
        if (response.data.msg === "It's a match!") {
          alert("It's a match!");
          this.fetchMatches();
        }
        this.fetchUsers();
      })
      .catch(error => {
        console.error(error);
      });
    },
    passUser(userId) {
      this.users = this.users.filter(user => user.id !== userId);
    },
  },
  created() {
    this.fetchUsers();
    this.fetchMatches();
  },
};
</script>

<style>
.user-card, .match-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 16px;
  text-align: center;
}

.user-photo, .match-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
</style>
