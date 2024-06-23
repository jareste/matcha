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
        <div>Personal description</div>
        <textarea v-model="text" maxlength="420" rows="5" cols="50"></textarea>
        <div v-if="descriptionError" class="error">{{ descriptionError }}</div>
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
    display: none;
}
</style>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            user: {
                username: '',//TODO no ensena ok el user y la foto
                photoUrl: ''
            },
            uploads: Array.from({ length: 5 }, () => ({ file: null, preview: null })),
            text: '',
            descriptionError: '',
        };
    },
    methods: {
        previewImage(event, index) {
            const file = event.target.files[0];
            this.uploads[index].file = file;
            this.uploads[index].preview = URL.createObjectURL(file);
        },
        validateDescription() {
            if (!this.text || this.text.trim().length === 0) {
                this.descriptionError = 'Description is required.';
                return false;
            } else if (this.text.length > 420) {
                this.descriptionError = 'Description must be less than 420 characters.';
                return false;
            } else {
                this.descriptionError = '';
                return true;
            }
        },
        async saveImages() {
            if (!this.validateDescription()) {
                return;
            }

            /**/
            const formData = new FormData();
            console.log('this.text---------------------------------------------------------------------------------');
            console.log('this.text', this.text);
            // formData.append(`text`, this.text);
            formData.append('text', this.text);
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            this.uploads.forEach((upload, index) => {
                if (upload.file) {
                    formData.append(`image${index}`, upload.file);
                }
            });

            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            this.uploads = Array.from({ length: 5 }, () => ({ file: null, preview: null }));

            /**/
            try {
                /* needs to be handled this way as i need to fetch profile again. */
                const response = await axios.post('http://localhost:5000/upload_photo', formData);
                console.log(response.data);

                await this.fetchUserPhotos();
            } catch (error) {
                console.error(error);
            }

        },
        async fetchUserPhotos() {
            try {
                axios.get('http://localhost:5000/user_photos')
                .then(response => {
                    console.log('aquiiiiiiiiiii', response.data);
                    response.data.photos.forEach((photo, index) => {
                        console.log('photo:', photo);
                        this.uploads[index].preview = 'http://localhost:5000/uploads/' + photo;
                    });
                    this.user.username = response.data.username;
                    this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
                    this.text = response.data.description;
                    this.isProfileLoaded = true;
                    console.log('responsedescription', response.data.description);
                });
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
