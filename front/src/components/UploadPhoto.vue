<template>
  <div>
    <form @submit.prevent="uploadPhoto">
      <input type="file" @change="onFileChange">
      <button type="submit">Upload</button>
    </form>

    <input type="text" v-model="photoName" placeholder="Enter photo name">
    <button @click="getPhoto">Show Photo</button>

    <input type="text" v-model="deletePhotoName" placeholder="Enter photo name to delete">
    <button @click="deletePhoto">Delete Photo</button>

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
      photoName: '',
      deletePhotoName: ''
    }
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0]
    },
    async uploadPhoto() {
      try {
        if (!this.selectedFile.type.startsWith('image/')) {
          throw new Error('File is not an image.')
        }

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
      } catch (error) {
        console.error(error)
      }
    },
    getPhoto() {
      if (this.photoName) {
        this.photoUrl = 'http://localhost:5000/uploads/' + this.photoName
      }
    },
    async deletePhoto() {
      if (this.deletePhotoName) {
        try {
          await axios.delete('http://localhost:5000/delete_photo/' + this.deletePhotoName)
          this.deletePhotoName = ''
        } catch (error) {
          console.log(error)
        }
      }
    }
  }
}
</script>
  