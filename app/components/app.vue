<template>
    <div class="grid-container">
        <div class="grid-x">
            <div class="app-grid-cell medium-6 medium-offset-3 cell">
                <div class="top-bar" v-if="hasToken()">
                    <div class="top-bar-left">
                        Joggr
                    </div>
                    <div class="top-bar-right">
                        <ul class="menu">
                            <li>
                                <a class="logout-button clear button" @click="logout()">Logout</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>


<script>
 export default {
     name: 'app',
     methods: {
         hasToken() {
             return !!localStorage.getItem('token')
         },
         logout() {
             localStorage.removeItem('token')
             this.$router.replace('/login')
         }
     }
 }
</script>

<style lang="scss" scoped>
 .app-grid-cell {
     border: solid 1px #ccc
 }

 .top-bar {
     background: #f9f9f9;

     .menu {
         background: transparent;
     }
 }
</style>
