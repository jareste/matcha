<template>
  <div>
    <h1>Recommended Users</h1>
    <div v-if="possible_match.id != -1"> <!-- v-if="possible_match"> -->
      <div class="user-container">
        <div v-for="possible_match in users" :key="possible_match.id" class="user-card" @click="goToProfile(possible_match.username)">
          <img :src="possible_match.photo" alt="User photo" class="user-photo" />
          <p>{{ possible_match.username }}</p>
          <button @click.stop="likeUser(possible_match.id)">Like</button>
          <button @click.stop="passUser(possible_match.id)">Pass</button>
        </div>
      </div>
    </div>
    <div v-if="possible_match.id == -1"> <!-- v-if="possible_match"> -->
      <h1 style="color: #ffffff; background-color: #688952;">No possible match found! Please leave our page!!!!</h1>
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
// import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      users: [],
      possible_match: {
        photo: '',
        username: '',
        id: -1,
      },
      matches: [],
      user: {
        id: 1, /* TODO update dynamically */
      },
    };
  },
  methods: {
    fetchUsers() {
      axios.get('http://localhost:5000/possible_match')
        .then(response => {
          if (response.data.msg == "KO")
          {
            this.possible_match.id = -1;
            return;
          }
          this.users = response.data.users;
          this.possible_match.id = 1;
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
        console.log('response', response.data.msg)
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
      axios.post('http://localhost:5000/dislike', {
        user_id: this.user.id,
        liked_user_id: userId,
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
    goToProfile(username) {
      this.$router.push(`/profile/${username}`);
    }
  },
  created() {
    this.fetchMatches();
    this.fetchUsers();
  },
};
</script>

<style>
.user-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.user-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 16px;
  text-align: center;
  width: 200px;
  cursor: pointer;
}

.user-photo, .match-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;

}
.match-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 16px;
  text-align: center;
  width: 200px;
}
</style>
