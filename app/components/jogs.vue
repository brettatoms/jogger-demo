<template>
</template>

<script>
 import VueRouter from 'vue-router'

 export default {
     beforeMount() {
         const token = localStorage.getItem('token')
         console.log(`token: ${token}`)
         if (!token) {
             return this.$router.replace('/login')
         }

         this.loadJogs();
     },

     methods: {
         loadJogs() {
             const token = localStorage.getItem('token')
             fetch('/api/jogs/', {
                 headers: {
                     'Authorization': `Token ${token}`
                 }
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 console.log(`data: ${data}`)
             }).catch((err) => {
                 // TODO: handle error
             })
         }
     }
 }
</script>

<style>
</style>
