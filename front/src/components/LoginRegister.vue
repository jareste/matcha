<template>
    <b-container>
      <p>{{ message }}</p>
      <b-row class="justify-content-center">
        <b-col cols="12" md="8">
          <b-card header="Please don't register" class="my-3">
            <router-view></router-view>
            <b-form @submit.prevent="login">
              <b-card-title>Login</b-card-title>
              <b-form-input type="text" v-model="loginForm.username" placeholder="Username"></b-form-input>
              <b-form-input type="password" v-model="loginForm.password" placeholder="Password"></b-form-input>
              <b-button type="submit" variant="primary">Login</b-button>
            </b-form>
  
            <b-form @submit.prevent="register" class="mt-3">
              <b-card-title>Register</b-card-title>
              <b-form-input type="text" v-model="registerForm.username" placeholder="Username"></b-form-input>
              <b-form-input type="text" v-model="registerForm.first_name" placeholder="First name"></b-form-input>
              <b-form-input type="text" v-model="registerForm.last_name" placeholder="Last name"></b-form-input>
              <b-form-input type="email" v-model="registerForm.email" placeholder="Email"></b-form-input>
              <b-form-input type="number" v-model="registerForm.age" placeholder="Age"></b-form-input>
              <b-form-input type="password" v-model="registerForm.password" placeholder="Password"></b-form-input>
              <b-form-input type="password" v-model="registerForm.passwordConfirmation" placeholder="Confirm Password"></b-form-input>
              <b-button type="submit" variant="primary">Register</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
    <b-footer class="mt-3 text-center">
      <p>Really, we don't want you here.</p>
    </b-footer>
  </template>
  
  <script>
  import axios from 'axios';
  import { inject } from 'vue';

  export default {
    data() {
      return {
        message: '',
        loginForm: {
          username: '',
          password: ''
        },
        registerForm: {
          username: '',
          email: '',
          age: '',
          password: '',
          passwordConfirmation: ''
        }
      }
    },
    setup () {
      const user = inject('user');
      return { user };
    },
    watch: {
        'registerForm.age'() {
        this.validateAge();
        },
    },
    methods: {
      login() {
        axios.post('http://localhost:5000/login', this.loginForm)
          .then(response => {
            if (response.data.error) {
              this.message = 'Error logging in: ' + response.data.description;
              return;
            }
            console.log(response.data);
            localStorage.setItem('token', response.data.access_token);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access_token;
            this.message = 'Login successful. Redirecting to upload photo page...';
            
            /**/
            this.user.username = response.data.username;
            this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
            this.user.isProfileLoaded = true;
            console.log('is loaded?',this.isProfileLoaded);

            /**/
            this.$router.push('/profile').catch(err => {
              console.error('Navigation error: ', err);
            });
          })
          .catch(error => {
            console.error(error);
            this.message = 'Error logging in: ' + error.response.data.description;
          });
      },
      validateAge() {
        if (!this.registerForm.age || this.registerForm.age < 18 || this.registerForm.age > 120) {
            this.message = 'Age must be between 18 and 120.';
            return false;
        } else {
            this.message = '';
            return true;
        }
      },
      register() {
        if (!this.validateAge())
          return;
        const user = {
          username: this.registerForm.username,
          first_name: this.registerForm.first_name,
          last_name: this.registerForm.last_name,
          email: this.registerForm.email,
          age: this.registerForm.age,
          password: this.registerForm.password,
          password_confirmation: this.registerForm.passwordConfirmation,
        };
        axios.post('http://localhost:5000/register', user)
          .then(response => {
            if (response.data.error) {
              this.message = 'Error registering: ' + response.data.description;
              return;
            }
            console.log(response.data);
            this.message = 'Registration successful. You can now login.';
          })
          .catch(error => {
            this.message = 'Error registering: ' + error.response.data.description;
            console.log(error);
          });
      }
    }
  }
  </script>