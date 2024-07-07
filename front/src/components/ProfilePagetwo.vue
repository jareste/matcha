<template>
  <div class="profile-page">
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <img :src="user.photoUrl" alt="User photo" class="profile-photo">
      <button @click="handleLikePass">{{ like_pass }}</button>
      <div class="photo-gallery">
        <div v-for="(upload, index) in user.uploads" :key="index" class="photo-container">
          <img v-if="upload.preview" :src="upload.preview" class="uploaded-photo" />
        </div>  
      </div>
      <div>Fame: {{ user.fame }}</div>
      <h2 class="username">{{ user.username }}</h2>
      <input type="text" v-model="user.first_name" readonly>
      <input type="text" v-model="user.last_name" readonly>
      <input type="text" v-model="user.email" readonly>
      <div>Profile enabled
        <input type="checkbox" :checked="user.enabled" disabled>
      </div>
      <div>Personal description</div>
      <textarea v-model="user.description" maxlength="420" rows="5" cols="40" readonly></textarea>
      <div>Gender</div>
      <select v-model="user.gender" disabled>
        <option value="no specified">No Specified</option>
        <option value="men">Men</option>
        <option value="woman">Woman</option>
      </select>
      <div>Preferred Gender</div>
      <select v-model="user.preferredGender" disabled>
        <option value="no specified">No Specified</option>
        <option value="men">Men</option>
        <option value="woman">Woman</option>
      </select>
      <div>Age: {{ user.age }}</div>
      <div>Age range</div>
      <div>
        <input type="number" v-model="user.ageMin" min="18" max="120" readonly>
        <input type="number" v-model="user.ageMax" min="18" max="120" readonly>
      </div>
      <div>Tags</div>
      <div class="spacing">
        <label v-for="tag in validTags" :key="tag">
          <input type="checkbox" :value="tag" v-model="user.selectedTags" disabled> {{ tag }}
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';
import { useRoute } from 'vue-router';

export default {
  data() {
    return {
      user: {
        id: 0,
        username: '',
        first_name: '',
        last_name: '',
        photoUrl: '',
        email: '',
        uploads: Array.from({ length: 5 }, () => ({ file: null, preview: null })),
        age: '',
        ageMin: 18,
        ageMax: 120,
        description: '',
        selectedTags: [],
        gender: 'no specified',
        preferredGender: 'no specified',
        enabled: false,
        fame: 0,
      },
      validTags: ['#sport', '#movies', '#series', '#gym', '#pets', '#cats', '#coding', '#food', '#party', '#videogames'],
      error: null,
      like_pass: 'like',
    };
  },
  setup() {
    const user_top = inject('user');
    return { user_top };
  },
  methods: {
    async fetchUserProfile(username) {
      try {
        const response = await axios.get(`http://localhost:5000/profile/${username}`);
        if (response.data.code === 401) {
          this.error = 'User not found';
          return;
        }
        this.error = null;
        const data = response.data;
        console.log(data);
        this.user.uploads = data.photos.map(photo => ({ preview: `http://localhost:5000/uploads/${photo}` }));
        this.user = {
          ...this.user,
          id: data.id,
          username: data.username,
          first_name: data.first_name,
          last_name: data.last_name,
          photoUrl: `http://localhost:5000/uploads/${data.photoUrl}`,
          email: data.email,
          age: data.age,
          ageMin: data.age_min || 18,
          ageMax: data.age_max || 120,
          description: data.description || '',
          selectedTags: data.tags ? data.tags.split(',') : [],
          gender: data.gender || 'no specified',
          preferredGender: data.prefered || 'no specified',
          enabled: data.enabled,
          fame: data.fame,
        };
        console.log('liked:', data.liked)
        this.like_pass = data.liked ? 'pass' : 'like';
        console.log('user:', this.user.uploads);
      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 401) {
          this.error = 'User not found';
        } else {
          this.error = 'An error occurred while fetching the profile';
        }
      }
    },
    handleLikePass() {
      const endpoint = this.like_pass === 'like' ? 'like' : 'dislike';
      console.log('endpoint:', endpoint);
      console.log('url:', `http://localhost:5000/${endpoint}`, {
        user_id: this.user.id
      })
      axios.post(`http://localhost:5000/${endpoint}`, {
        liked_user_id: this.user.id
      })
      .then(response => {
        console.log(response.data);
        this.like_pass = this.like_pass === 'like' ? 'pass' : 'like';
      })
      .catch(error => {
        console.error(error);
      });
    }
  },
  created() {
    const route = useRoute();
    const username = route.params.username;
    this.fetchUserProfile(username);
  },
  watch: {
    '$route.params.username': {
      immediate: true,
      handler(newUsername) {
        this.fetchUserProfile(newUsername);
      }
    }
  }
};
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-photo {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
}

.photo-gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.uploaded-photo {
  width: 100px;
  height: 100px;
  object-fit: cover;
}

.checkbox {
  display: flex;
  align-items: center;
}

.error {
  color: red;
  margin-top: 10px;
}

.spacing {
  margin-bottom: 50px;
}
</style>
