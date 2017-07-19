<template>
    <div class="signup-container grid-container">
        <div class="grid-x">
            <div class="small-10 small-offset-1 cell">
                <form id="signup-form" @keyup.13="signup()">
                    <label>Username
                        <input type="text" name="username" v-model="username"/>
                        <inline-errors :errors="errors['username']"></inline-errors>
                    </label>
                    <label>Password
                        <input type="password" name="password1" v-model="password1"/>

                        <inline-errors :errors="errors['password1']"></inline-errors>
                    </label>

                    <label>Confirm Password
                        <input type="password" name="password2" v-model="password2"/>
                        <inline-errors :errors="errors['password2']"></inline-errors>
                    </label>

                    <button
                        class="signup-button button"
                        type="button"
                        @click="signup()"
                        :disabled="username && password1 && password2 ? false : true"
                    >Signup</button>
                    <router-link to="/login" class="login-button clear button">Login</router-link>
                </form>

                <inline-errors :errors="errors['non_field_errors']"></inline-errors>
                <p class="error-message">{{ errors.detail }}</p>
            </div>
        </div>
    </div>
</template>

<script>
 export default {
     data: function() {
         return {
             username: null,
             password1: null,
             password2: null,
             errors: {}
         }
     },
     methods: {
         signup() {
             // don't do anything if we don't have a username and password
             if (!this.$data.username || !this.$data.password1 || !this.$data.password2) return;

             this.$http.post('/api/auth/register', {
                 username: this.$data.username,
                 password1: this.$data.password1,
                 password2: this.$data.password2,
             })
                 .then((response) => {
                     return response.json().then((data) => [response, data])
                 })
                 .then((response_data) => {
                     const [response, data] = response_data
                     this.$store.commit('setCurrentUser', data.user)
                     this.$store.commit('setToken', data.token)
                     this.$router.replace('/')
                 }).catch((err) => {
                     console.error(err)
                     const contentType = err.headers ? err.headers.map['Content-Type'] : []
                     if (contentType.includes('application/json')) {
                         err.json().then((data) => this.$data.errors = data)
                     } else {
                         this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
                     }
                 })
         }
     }
 }
</script>

<style lang="scss" scoped>
 .signup-container {
     margin-top: 20px;
 }

 input[name=password] {
     margin-bottom: 0;
 }

 .signup-button {
     margin-top: 28px;
 }

 .button {
     width: 100%;
 }


 .error-message {
     color: red;
 }
</style>
