<template>
    <div class="grid-container">
        <div class="grid-x">
            <div class="app-grid-cell medium-6 medium-offset-3 cell">
                <div class="top-bar" v-if="hasToken()">
                    <div class="top-bar-left">
                        Joggr
                    </div>
                    <div class="top-bar-right">
                        <ul
                            v-dropdown-menu
                            class="dropdown menu"
                            data-dropdown-menu
                            data-alignment="right"
                            data-click-open="true"
                        >
                            <li>
                                <a class="menu-text" href="">{{ currentUserName }}</a>
                                <ul class="menu">
                                    <li>
                                        <router-link
                                            :to="{ path: '/users/edit', query: { id: currentUserId }}"
                                        >Profile</router-link>
                                    </li>
                                    <li>
                                        <router-link to="/users">Users</router-link>
                                    </li>
                                    <li><a @click="logout()">Logout</a></li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
                <router-view :key="$route.fullPath"></router-view>
            </div>
        </div>
    </div>
</template>


<script>
 import Vue from 'vue'
 import 'foundation-sites'
 import $ from 'jquery';

 export default {
     name: 'app',
     directives: {
         'dropdown-menu': {
             bind(el) {
                 new Foundation.DropdownMenu($(el))
             },
             unbind(el) {
                 $(el).foundation('_destroy')
             }
         }
     },
     computed: {
         currentUserId() {
             return this.$store.state.currentUser.id
         },
         currentUserName() {
             return this.$store.state.currentUser.username
         }
     },
     methods: {
         hasToken() {
             return !!this.$store.state.token
         },
         logout() {
             this.$store.commit('logout')
             this.$router.replace('/login')
         }
     }
 }
</script>

<style lang="scss" scoped>

 $top-bar-bg: #f9f9f9;

 .app-grid-cell {
     border: solid 1px #ccc
 }

 .top-bar {
     background: $top-bar-bg;

     .menu-text {
         font-weight: normal;
         background: $top-bar-bg;
     }
     .menu {
         background: white;
     }
 }
</style>
