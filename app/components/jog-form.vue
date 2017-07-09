<template>
    <!-- <div class="top-bar"> -->
    <!-- Joggr -->
    <!-- </div> -->
</template>

<script>
 import VueRouter from 'vue-router'

 export default {
     beforeMount() {
         console.log('beforeMount()')
         const token = localStorage.getItem('token')
         console.log(`token: {token}`)
         console.log(this)
         if (!token) {
             this.$router.replace('/login')
         }
     },

     methods: {
         login() {
             console.log('login()')
         }
     }
 }
</script>

<style>
 .top-bar {
     text-align: center;
 }
</style>
