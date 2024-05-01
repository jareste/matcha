<template>
    <div class="profile-page">
        <img :src="user.photoUrl" alt="User photo" class="profile-photo">
        <h2 class="username">{{ user.username }}</h2>

        <div class="photo-upload-container">
            <div class="photo-upload" v-for="(upload, index) in uploads" :key="index">
                <label :for="'file-upload-' + index" class="custom-file-upload">
                    <img :src="upload.preview" class="preview-photo" v-if="upload.preview">
                    <div class="plus-sign" v-else>+</div>
                </label>
                <input :id="'file-upload-' + index" type="file" @change="previewImage($event, index)" class="file-input">
            </div>
        </div>

        <button @click="saveImages">Save</button>
    </div>
</template>

<style scoped>

.profile-page {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.photo-upload-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.custom-file-upload {
    width: 200px;
    height: 200px;
    margin: 15px;
    border: 1px solid #00fb71;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #060000;
}

.plus-sign {
    font-size: 50px;
}

.preview-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.file-input {
    display: none; /* Hide the file input */
}
</style>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            user: {
                username: '',
                photoUrl: ''
            },
            uploads: Array.from({ length: 5 }, () => ({ file: null, preview: null })) // Initialize an array of 5 unique upload slots
        };
    },
    methods: {
        previewImage(event, index) {
            const file = event.target.files[0];
            this.uploads[index].file = file;
            this.uploads[index].preview = URL.createObjectURL(file);
        },
        async saveImages() {
            const formData = new FormData();
            this.uploads.forEach((upload, index) => {
                if (upload.file) {
                    formData.append(`image${index}`, upload.file);
                }
            });
            axios.post('http://localhost:5000/upload_photo', formData)
                .then(response => {
                    console.log(response.data); //not handled
                })
                .catch(error => {
                    console.error(error);
                });
        },
        async fetchUserPhotos() {
            try {
                axios.get('http://localhost:5000/user_photos')
                .then(response => {
                    console.log(response.data);
                    response.data.photos.forEach((photo, index) => {
                        console.log('photo:', photo);
                        this.uploads[index].preview = 'http://localhost:5000/uploads/' + photo;
                    });
                    // this.user.username = response.data.username;
                    // this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
                });
                // // console.log(response.data);
                // // response.data.photos.forEach((photo, index) => {
                // //     console.log('photo:', photo.url);
                // //     this.uploads[index].preview = photo.url;
                // });
            } catch (error) {
                console.error(error);
            }
        }
    },
    created() {
        this.fetchUserPhotos();
    }
};
</script>

<!-- Add your existing styles here -->