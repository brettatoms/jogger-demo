<template>
    <div class="job-form-container grid-container">
        <div class="grid-x">
            <div class="medium-8 medium-offset-2 cell">
                <h5 v-if="!user.id">Create new user</h5>
                <form id="user-form">
                    <label>Username
                        <input type="text" v-model="user.username"/>
                        <inline-errors :errors="errors['username']"></inline-errors>
                    </label>
                    <label>Role
                        <select v-model="user.role">
                            <option value="user">user</option>
                            <option value="manager">manager</option>
                            <option value="admin">admin</option>
                        </select>
                        <inline-errors :errors="errors['role']"></inline-errors>
                    </label>

                    <div v-if="!user.id">
                        <label>Password
                            <input type="password" v-model="password1"/>
                            <inline-errors :errors="errors['password']"></inline-errors>
                        </label>

                        <label>Confirm Password
                            <input type="password" v-model="password2"/>
                        </label>
                    </div>

                    <div class="actions grid-x align-justify" v-if="!confirmDelete">
                        <div class="cell small-4">
                            <a v-if="user.id" class="alert clear button" @click="confirmDelete=true">Delete</a>
                        </div>
                        <div class="text-right cell small-6">
                            <a class="clear button" @click="cancel()">Cancel</a>
                            <a class="button" @click="save()">Save</a>
                        </div>
                    </div>

                    <div class="confirm-delete-container grid-x align-justify" v-if="confirmDelete">
                        <p class="cell small-6">Are you sure you want to delete this user?</p>
                        <div class="text-right cell small-6">
                            <a class="clear button" @click="confirmDelete=false">No</a>
                            <a class="delete-yes-button alert button" @click="remove()">Yes</a>
                        </div>
                    </div>
                </form>

                <form class="change-password-form" v-if="user.id">
                    <label>Password
                        <input type="password" v-model="password1"/>
                        <inline-errors :errors="errors['new_password1']"></inline-errors>
                    </label>


                    <label>Confirm Password
                        <input type="password" v-model="password2"/>
                        <inline-errors :errors="errors['new_password2']"></inline-errors>
                    </label>

                    <div class="actions grid-x align-right" v-if="!confirmDelete">
                        <div class="text-right cell small-6">
                            <a class="button" @click="changePassword()">Change password</a>
                        </div>
                    </div>
                </form>
                <inline-errors :errors="errors['non_field_errors']"></inline-errors>
            </div>
        </div>
    </div>
</template>

<script>
 import VueRouter from 'vue-router'
 import toastr from 'toastr'

 export default {
     data: function() {
         return {
             user: { role: 'user' },
             password1: null,
             password2: null,
             errors: { },
             confirmDelete: false
         }
     },

     created() {
         if (!this.$route.query.id) {
             return
         }

         // get jog details
         const userId = this.$route.query.id
         this.$http.get(`/api/users/${userId}/`)
             .then((response) => {
                 if (response.status !== 200) {
                     console.log(response.data)
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                     return;
                 }

                 return response
                     .json()
                     .then((data) => this.$data.user = data)
             }).catch((err) => {
                 console.log(err)
                 this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
             })
     },

     methods: {
         cancel() {
             this.$router.back()
         },

         changePassword() {
             this.$data.errors = { }
             this.$http.post('/api/auth/password/change/', {
                 new_password1: this.$data.password1,
                 new_password2: this.$data.password2
             }).then((response) => {
                 toastr.success('Password changed')
             }).catch((err) => {
                 console.log(err)
                 const contentType = err.headers ? err.headers.map['Content-Type'] : []
                 if (contentType.includes('application/json')) {
                     err.json().then((data) => { this.$data.errors = data; console.log(this.$data.errors) })
                 } else {
                     this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
                 }
             })
         },

         save() {
             let method = 'post'
             let url = '/api/users/'
             if (this.$data.user.id) {
                 method = 'put'
                 url = `${url}${this.$data.user.id}/`
             }

             const data = {
                 username: this.$data.user.username,
                 role: this.$data.user.role
             }

             // set the password if the user entered one
             if (this.$data.password1 && (this.$data.password1 == this.$data.password2)) {
                 data.password = this.$data.password1
             }

             this.$data.errors = { }
             this.$http[method](url, data)
                 .then((response) => {
                     if (!response.ok) {
                         this.$data.errors = response.body
                         return;
                     }

                     toastr.success('User saved')

                     return response
                         .json()
                         .then((user) => {
                             const mutation =  method === 'post' ? 'addUser' : 'updateUser'
                             this.$store.commit(mutation, user)

                             // go back in history if we just create a user
                             if (method === 'post') {
                                 this.$router.back(); // pop router history
                             }
                         })
                 })
                 .catch((err) => {
                     console.log(err)
                     const contentType = err.headers ? err.headers.map['Content-Type'] : []
                     if (contentType.includes('application/json')) {
                         err.json().then((data) => { this.$data.errors = data; console.log(this.$data.errors) })
                     } else {
                         this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
                     }
                 })
         },

         remove() {
             const userId = this.$data.user.id;
             this.$http.delete(`/api/users/${userId}/`)
                 .then((response) => {
                     if (!response.ok) {
                         /* this.$data.errors = response.body*/
                         console.error(response.body)
                         return;
                     }

                     toastr.success('User deleted')
                     this.$store.commit('deleteUser', userId)
                     this.$router.back(); // pop router history
                 }).catch((err) => {
                     console.error(err)
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                 })
                 .then(() => this.confirmDelete = false)
         }
     }
 }
</script>

<style lang="scss" scoped>
 h5 {
     margin-top: 12px;
 }

 .confirm-delete-container {
     padding: 10px;
     margin: 10px 0;
     background: #cc4b37;
     color: white;

     .button {
         color: white;
     }
 }

 .delete-yes-button {
     border: solid 1px white;
 }

 .change-password-form {
     margin-top: 20px;
 }

</style>
