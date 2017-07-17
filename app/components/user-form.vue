<template>
    <div class="job-form-container grid-container">
        <div class="grid-x">
            <div class="medium-8 medium-offset-2 cell">
                <form id="user-form">
                    <label>Username
                        <input type="text" v-model="user.username"/>
                        <p
                            v-for="msg in errors['date']"
                            class="alert help-text"
                        >{{ msg }}</p>
                    </label>
                    <label>Role
                        <select v-model="user.role">
                            <option value="user">user</option>
                            <option value="manager">manager</option>
                            <option value="admin">admin</option>
                        </select>
                        <p
                            v-for="msg in errors['date']"
                            class="alert help-text"
                        >{{ msg }}</p>
                    </label>


                    <div class="actions grid-x align-justify" v-if="!confirmDelete">
                        <div class="cell small-4">
                            <a class="alert clear button" @click="confirmDelete=true">Delete</a>
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

                <form>
                    <label>Confirm Password
                        <input type="password" name="confirm_password" v-model="confirmPassword"/>
                        <p
                            v-for="msg in errors['confirm_password']"
                            class="alert help-text"
                        >{{ msg }}</p>
                    </label>

                    <label>Password
                        <input type="password" name="password1" v-model="password1"/>
                        <p
                            v-for="msg in errors['password1']"
                            class="alert help-text"
                        >{{ msg }}</p>
                    </label>


                    <label>Confirm Password
                        <input type="password" name="password2" v-model="password2"/>
                        <p
                            v-for="msg in errors['password2']"
                            class="alert help-text"
                        >{{ msg }}</p>
                    </label>

                </form>
                <p
                    v-for="msg in errors['non_field_errors']"
                    class="alert"
                >{{ msg }}</p>
            </div>
        </div>
    </div>
</template>

<script>
 import VueRouter from 'vue-router'

 export default {
     data: function() {
         return {
             user: { },
             password1: null,
             password2: null,
             errors: { },
             confirmDelete: false
         }
     },

     created() {
         this.$data.userId = this.$route.query.id
         if (!this.$route.query.id) {
             return
         }
         // get jog details
         this.$http.get(`/api/users/${this.$route.query.id}/`)
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
             this.$http('/api/auth/password/change', {
                 new_password1: this.$data.password1,
                 new_password2: this.$data.password2,
                 old_password: this.$data.confirmPassword
             }).then((response) => {
                 /* TODO  */
             })
         },

         save() {
             let method = 'post'
             let url = '/api/users/'
             if (this.$data.userId) {
                 method = 'put'
                 url = `${url}${this.$data.userId}/`
             }

             const data = {
                 username: this.$data.user.username,
                 role: this.$data.user.role
             }

             // set the password if the user entered one
             if (this.$data.password1 && (this.$data.password1 == this.$data.password2)) {
                 data.password1 = this.$data.password1
                 data.password2 = this.$data.password2
             }

             this.$http[method](url, data)
                 .then((response) => {
                     if (response.status !== 200) {
                         this.$data.errors = response.body
                         return;
                     }

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
                     console.error(err)
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                 })
         },

         remove() {
             this.$http.delete(`/api/users/${this.$data.userId}/`)
                 .then((response) => {
                     if (response.status !== 200) {
                         /* this.$data.errors = response.body*/
                         console.error(response.body)
                         return;
                     }

                     this.$store.commit('deleteUser', this.$data.userId)
                     this.$router.back(); // pop router history
                 }).catch((err) => {
                     console.error(err)
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                 })
         }
     }
 }
</script>

<style lang="scss" scoped>
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

</style>
