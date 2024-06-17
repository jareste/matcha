<template>
  <div>
    <h1>Find Your Match</h1>
    <div> <!-- v-if="possible_match"> -->
        <img :src="possible_match.photo" alt="User photo" class="user-photo" />
        <p>{{ possible_match.username }}</p>
        <button @click="likeUser(user.id)">Like</button>
        <button @click="passUser(user.id)">Pass</button>
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
      // users: [],
      possible_match: {
        photo: '',
        username: '',
        id: '',
      },
      matches: [],
      user: {
        id: 1,
      },
    };
  },
  methods: {
    fetchUsers() {
      axios.get('http://localhost:5000/possible_match')
        .then(response => {
          console.log('sisisisisii', response.data);
          this.possible_match.id = response.data.user;
          this.possible_match.username = response.data.username;
          this.possible_match.photo = 'http://localhost:5000/uploads/' + response.data.user_photo;
          console.log('ussers', this.users);
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchMatches() {
      axios.get(`http://localhost:5000/matches/${this.user.id}`)
        .then(response => {
          console.log('sisisisisii41414123');
          this.matches = response.data.matches;
          console.log('matches', this.matches);
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
  },
  created() {
    this.fetchMatches();
    this.fetchUsers();
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
