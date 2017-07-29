<template>
    <div class="grid-container">
        <div class="grid-x">
            <div class="medium-2 medium-offset-1 large-2 large-offset-1 cell">
                <side-bar></side-bar>
            </div>
            <div class="app-grid-cell small-12 medium-6 large-6 cell">
                <!-- <top-bar></top-bar> -->
                <router-view :key="$route.fullPath"></router-view>
            </div>
        </div>
    </div>
</template>


<script>
 import Vue from 'vue'
 import 'foundation-sites'

 export default {
     name: 'app',
 }
</script>

<style lang="scss" scoped>
 .app-grid-cell {
     border: solid 1px #ccc;
     padding-bottom: 20px;
 }


</style>
