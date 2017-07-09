<template>
    <div class="grid-container">
        <div class="top-bar" v-if="hasToken()">
            Joggr
        </div>
        <router-view></router-view>
    </div>
</template>


<script>
 export default {
     name: 'app',
     methods: {
         hasToken() {
             return !!localStorage.getItem('token')
         }
     }
 }
</script>

<style>
 .top-bar {
     text-align: center;
     background: #f9f9f9;
     padding: 8px 0;
 }
</style>
