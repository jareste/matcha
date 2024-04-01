<template>
    <div class="profile-page">
        <img :src="user.photoUrl" alt="User photo" class="profile-photo">
        <h2 class="username">{{ user.username }}</h2>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            user: {
                username: '',
                photoUrl: ''
            }
        }
    },
    created() {
        axios.get('http://localhost:5000/getProfile')
            .then(response => {
                this.user.username = response.data.username;
                this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
                console.log("photo: " + this.user.photoUrl);
            })
            .catch(error => {
                console.error(error);
            });
    }
}
</script>

<style scoped>
.profile-page {
    text-align: center;
}

.profile-photo {
    width: 200px;
    height: 200px;
    border-radius: 50%;
}

.username {
    margin-top: 20px;
    font-size: 24px;
}
</style>