<template>
    <div>
        <section id="jog-section">
            <h1>Jogs</h1>
            <ul>
                <li><router-link to="/">Jog list</router-link></li>
                <li><router-link :to="'/add?userId=' + userId">Add Jog</router-link></li>
                <li><router-link to="/report">Report</router-link></li>
            </ul>
        </section>
        <section id="user-section">
            <h1>Users</h1>
            <ul>
                <li><router-link to="/users">User list</router-link></li>
                <li><router-link to="/users/add">Add User</router-link></li>
            </ul>
        </section>
        <section id="user-section">
            <h1>Profile</h1>
            <ul>
                <li>
                    <router-link
                        :to="{ path: '/users/edit', query: { id: currentUserId }}"
                    >Settings</router-link>
                <li><a @click="logout()">Logout</a></li>
            </ul>
        </section>
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
 @import '~foundation-sites/scss/util/util';

 h1 {
     font-size: rem-calc(20);
     background: #1779ba;
     color: white;
     padding: 4px 8px;
 }

 h1:nth-child(n+2) {
     margin-top: 10px;
 }

 ul {
     margin-left: 0
 }

 li {
     list-style: none;
 }

 a {
     display: block;
 }

</style>
