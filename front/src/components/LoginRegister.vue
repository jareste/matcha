<template>
    <b-container>
      <p>{{ message }}</p>
      <b-row class="justify-content-center">
        <b-col cols="12" md="8">
          <b-card header="Vue.js Authentication" class="my-3">
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
              <b-form-input type="email" v-model="registerForm.email" placeholder="Email"></b-form-input>
              <b-form-input type="password" v-model="registerForm.password" placeholder="Password"></b-form-input>
              <b-form-input type="password" v-model="registerForm.passwordConfirmation" placeholder="Confirm Password"></b-form-input>
              <b-button type="submit" variant="primary">Register</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
    <b-footer class="mt-3 text-center">
      <p>Vue.js Authentication</p>
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
          password: '',
          passwordConfirmation: ''
        }
      }
    },
    setup () {
      const user = inject('user');
      return { user };
    },
    methods: {
      login() {
        axios.post('http://localhost:5000/login', this.loginForm)
          .then(response => {
            console.log(response.data);
            localStorage.setItem('token', response.data.access_token);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access_token;
            this.message = 'Login successful. Redirecting to upload photo page...';
            
            // updated with the inject property
            this.user.username = response.data.username;
            this.user.photoUrl = 'http://localhost:5000/uploads/' + response.data.photoUrl;
          })
          .catch(error => {
            console.error(error);
            this.message = 'Error logging in: ' + error.response.data.description;
          });
      },
      register() {
        const user = {
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
          password_confirmation: this.registerForm.passwordConfirmation,
        };
        console.log(user);
        axios.post('http://localhost:5000/register', user)
          .then(response => {
            console.log(response.data);
            this.message = 'Registration successful. You can now login.';
          })
          .catch(error => {
            this.message = 'Error registering: ' + error.response.data.description;
            console.error(error);
          });
      }
    }
  }
  </script>