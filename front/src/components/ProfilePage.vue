<template>
  <div class="profile-page">
    <img :src="user.photoUrl" alt="User photo" class="profile-photo">
    <div>Fame: {{fame}}</div>
    <!-- <h2 class="username">{{ user.username }}</h2> -->
    <input type="text" v-model="user.username">
    <input type="text" v-model="user.first_name">
    <input type="text" v-model="user.last_name">
    <input type="text" v-model="user.email">
    <!-- <h2 class="name">{{ user.first_name }} {{ user.last_name }}</h2> -->

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

    <div>Gender</div>
    <select v-model="gender">
      <option value="no specified">No Specified</option>
      <option value="men">Men</option>
      <option value="woman">Woman</option>
    </select>

    <div>Preferred Gender</div>
    <select v-model="preferredGender">
      <option value="no specified">No Specified</option>
      <option value="men">Men</option>
      <option value="woman">Woman</option>
    </select>

    <div>Age: {{age}}</div>
    <div>Age range </div>

    <div>
        <input type="number" v-model="ageMin" min="18" max="120" placeholder="Min Age">
        <input type="number" v-model="ageMax" min="18" max="120" placeholder="Max Age">
        <div v-if="ageError" class="error">{{ ageError }}</div>
    </div>

    <div>Tags</div>
    <div>
      <label v-for="tag in validTags" :key="tag">
        <input type="checkbox" :value="tag" v-model="selectedTags"> {{ tag }}
      </label>
    </div>

    <button @click="saveImages" class="save-button">Save Information</button>
  </div>
</template>

<style scoped>

.save-button {
    display: flex;
    margin-bottom: 60px;
}

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
    width: 150px;
    height: 150px;
    margin: 10px;
    border-radius: 50%;
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
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
}

.profile-photo {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 50%;
}

.file-input {
    display: none;
}

.error {
    color: rgb(201, 0, 191);
}
</style>

<script>
import axios from 'axios';
import { inject } from 'vue';

export default {
    data() {
        return {
            user: {
                username: '',
                first_name: '',
                last_name: '',
                photoUrl: '',
                email: ''
            },
            ageMin: 18,
            ageMax: 120,
            uploads: Array.from({ length: 5 }, () => ({ file: null, preview: null })),
            text: '',
            descriptionError: '',
            validTags: ['#sport', '#movies', '#series', '#gym', '#pets', '#cats', '#coding', '#food',
        '#party', '#sport', '#videogames'],
            selectedTags: [],
            gender: 'no specified',
            preferredGender: 'no specified',
            age: '',
            ageError: '',
            fame: 0,
        };
    },
    setup () {
      const user_top = inject('user');
      return { user_top };
    },
    watch: {
        ageMin() {
        this.validateAgeRange();
        },
        ageMax() {
        this.validateAgeRange();
        },
    },
    methods: {
        previewImage(event, index) {
            const file = event.target.files[0];
            this.uploads[index].file = file;
            this.uploads[index].preview = URL.createObjectURL(file);
        },
        validateAgeRange() {
            if (Number(this.ageMin) < 18 || Number(this.ageMax) > 120 || Number(this.ageMin) > Number(this.ageMax)) {
                this.ageError = "Invalid age range. Must be between 18 and 120 and min must be <= max.";
            } else {
                this.ageError = null;
            }
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
        validateAge() {
            if (!this.age || this.age < 18 || this.age > 120) {
                this.ageError = 'Age must be between 18 and 120.';
                return false;   
            } else {
                this.ageError = '';
                return true;
            }
        },
        async saveImages() {
            if (!this.validateDescription() || !this.validateAge()) {
                return;
            }

            /**/
            const formData = new FormData();
            console.log('this.text---------------------------------------------------------------------------------');
            console.log('this.text', this.text);


            formData.append('gender', this.gender);
            formData.append('username', this.user.username);
            formData.append('first_name', this.user.first_name);
            formData.append('last_name', this.user.last_name);
            formData.append('ageMax', this.ageMax);
            formData.append('ageMin', this.ageMin);
            formData.append('email', this.user.email);
            formData.append('preferredGender', this.preferredGender);
            formData.append('text', this.text);
            /*DEBUG*/
            // for (let [key, value] of formData.entries()) {
            //     console.log(`${key}: ${value}`);
            // }

            /**/
            formData.append('tags', this.selectedTags.join(','));
            this.uploads.forEach((upload, index) => {
                if (upload.file) {
                    formData.append(`image${index}`, upload.file);
                }
            });

            /*DEBUG*/
            // for (let [key, value] of formData.entries()) {
            //     console.log(`${key}: ${value}`);
            // }
            this.uploads = Array.from({ length: 5 }, () => ({ file: null, preview: null }));

            /**/
            try {
                /* needs to be handled this way as i need to fetch profile again. */
                const response = await axios.post('http://localhost:5000/upload_photo', formData);
                console.log('response', response.data);

                if (response.data.access_token) {
                    localStorage.setItem('token', response.data.access_token);
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access_token;
                }

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
                    this.user_top.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;

                    this.user_top.username = response.data.username;
                    this.ageMax = response.data.age_max? response.data.age_max: "120";
                    this.ageMin = response.data.age_min? response.data.age_min: "18";
                    this.ageError = '';
                    this.user.email = response.data.email;
                    this.user.first_name = response.data.first_name;
                    this.fame = response.data.fame;
                    this.user.last_name = response.data.last_name;
                    this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
                    this.text = response.data.description? response.data.description: "Add your description here";
                    this.selectedTags = response.data.tags ? response.data.tags.split(',') : [];
                    this.gender = response.data.gender ? response.data.gender : "no specified";
                    this.preferredGender = response.data.prefered? response.data.prefered : "no specified";
                    this.age = response.data.age? response.data.age: "18";
                    this.isProfileLoaded = true;
                    console.log('responsedescription', response.data.age);
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
