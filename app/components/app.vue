<template>
    <div class="grid-container">
        <div class="grid-x">
            <div class="app-grid-cell medium-6 medium-offset-3 cell">
                <top-bar></top-bar>
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
