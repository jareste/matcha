<template>
  <div>
    <nav>
      <router-link to="/login-register">Login/Register</router-link> |
      <router-link to="/upload-photo">Upload Photo</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  // ...
}
</script>