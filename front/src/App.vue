<template>
  <div>
    <button @click="fetchData">Fetch Data</button>
    <button @click="fetchData1">Fetch Dasta1</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/api/data')
        .then(response => {
          console.log('Hello Worlsd');
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchData1() {
      axios.get('http://localhost:5000/api/bye')
        .then(response => {
          console.log('sadge');
          console.log(response.data);
          console.log('sadge');
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>