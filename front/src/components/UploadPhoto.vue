<template>
    <div>
      <form @submit.prevent="uploadPhoto">
        <input type="file" @change="onFileChange">
        <button type="submit">Upload</button>
      </form>
  
      <input type="text" v-model="photoName" placeholder="Enter photo name">
      <button @click="getPhoto">Show Photo</button>
  
      <img :src="photoUrl" v-if="photoUrl">
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        selectedFile: null,
        photoUrl: null,
        photoName: ''
      }
    },
    methods: {
      onFileChange(e) {
        this.selectedFile = e.target.files[0]
      },
      async uploadPhoto() {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
  
        const response = await axios.post('http://localhost:5000/upload_photo', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
  
        if (response.data) {
          this.photoName = this.selectedFile.name
        }
      },
      getPhoto() {
        if (this.photoName) {
          this.photoUrl = 'http://localhost:5000/uploads/' + this.photoName
        }
      }
    }
  }
  </script>
  