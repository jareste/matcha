<template>
    <b-container>
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
  
  export default {
    data() {
      return {
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
    methods: {
      login() {
        axios.post('http://localhost:5000/login', this.loginForm)
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.error(error);
          });
      },
      register() {
        const user = {
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
          password_confirmation: this.registerForm.passwordConfirmation,  // Change this line
        };
        console.log(user);
        axios.post('http://localhost:5000/register', user)
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.error(error);
          });
      }
    }
  }
  </script>