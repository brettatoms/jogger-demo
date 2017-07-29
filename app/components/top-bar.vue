<template>
    <div class="top-bar" v-if="hasToken()">
        <div class="top-bar-left">
            <router-link to="/" class="title-link">Joggr</router-link>
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
                            <router-link to="/report">Report</router-link>
                        </li>
                        <li v-if="showUsersMenuItem">
                            <router-link to="/users">Users</router-link>
                        </li>
                        <li><a @click="logout()">Logout</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
 import $ from 'jquery';

 export default {
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
         },
         showUsersMenuItem() {
             const role = this.$store.state.currentUser.role
             return ['manager', 'admin'].includes(role)
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

 .title-link {
     color: black;

     &:hover {
         color: #666;
     }
 }
</style>
