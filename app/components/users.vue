<template>
    <div>
        <router-link class="clear button" to="/users/add" v-if="users.length">Add User</router-link>
        <table class="user-table" v-if="users.length">
            <thead>
                <tr>
                    <th><a @click="sortBy('username')">Username</a></th>
                    <th><a @click="sortBy('role')">Role</a></th>
                </tr>
            </thead>
            <tbody>
                <tr class="jog-row" v-for="user in users" @click="editUser(user)">
                    <td>{{ user.username }}</td>
                    <td>{{ user.role }}</td>
                    <td v-if="isAdmin"><a @click.prevent.stop="viewJogs(user) ">view jogs</a></td>
                </tr>
            </tbody>
        </table>
        <div class="empty-state" v-if="!users.length">
            <router-link to="/users/add" class="button">Add User</router-link>
        </div>
    </div>
</template>

<script>
 import moment from 'moment';
 import VueRouter from 'vue-router'
 import orderBy from 'lodash.orderby'

 export default {
     data: function() {
         return {
             sortKey:  'date',
             sortAsc: true,
         }
     },
     beforeMount() {
         this.loadUsers();
     },

     computed: {
         users() {
             return this.$store.state.users
         },
         isAdmin() {
             return this.$store.state.currentUser.role == 'admin'
         }
     },

     methods: {
         sortBy(key) {
             const sortKey = {
                 date: 'date',
                 distance: 'distance_in_feet',
                 time: 'time_in_seconds'
             }[key];

             // reverse the sort order if we're already sorting by this key
             if (this.sortKey === sortKey) {
                 this.sortAsc = !this.sortAsc
             } else {
                 this.sortKey = sortKey
                 this.sortAsc = true
             }
         },

         loadUsers() {
             this.$http.get('/api/users/')
                 .then((response) => {
                     return response.json().then(data => [response, data])
                 }).then((response_data) => {
                     const [response, data] = response_data
                     this.$store.commit('setUsers', data)
                 }).catch((err) => {
                     // TODO: handle error
                 })
         },

         editUser(user) {
             this.$router.push({
                 path: '/users/edit',
                 query: { id: user.id }
             })
         },

         viewJogs(user) {
             this.$router.push({
                 path: '/',
                 query: { user_id: user.id }
             })
         }
     }
 }
</script>

<style lang="scss" scoped>
 .user-table {
     width: 100%;


     th, td {
         text-align: left;
         padding-left: 10px;
     }

     tbody {
         tr {
             &:hover {
                 text-decoration: underline;
                 cursor: pointer;
                 background: #eee;
             }
         }
     }
 }

 .empty-state {
     text-align: center;
     margin: 20px;
 }
</style>
