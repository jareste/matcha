<template>
  <div>
    <form @submit.prevent="login">
      <h2>Login</h2>
      <input type="text" v-model="loginForm.username" placeholder="Username">
      <input type="password" v-model="loginForm.password" placeholder="Password">
      <button type="submit">Login</button>
    </form>

    <form @submit.prevent="register">
      <h2>Register</h2>
      <input type="text" v-model="registerForm.username" placeholder="Username">
      <input type="email" v-model="registerForm.email" placeholder="Email">
      <input type="password" v-model="registerForm.password" placeholder="Password">
      <input type="password" v-model="registerForm.passwordConfirmation" placeholder="Confirm Password">
      <button type="submit">Register</button>
    </form>
  </div>
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