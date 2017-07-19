<template>
    <div class="login-container grid-container">
        <div class="grid-x">
            <div class="small-10 small-offset-1 cell">
                <form id="login-form" @keyup.13="login()">
                    <label>Username
                        <input type="text" name="username" v-model="username"/>
                        <p
                            v-for="msg in errors['username']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>

                    <label>Password
                        <input type="password" name="password" v-model="password"/>
                        <p
                            v-for="msg in errors['password']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>
                    <!-- <a class="forgot-password-link">Forgot your password?</a> -->
                    <button
                        class="login-button button"
                        type="button"
                        @click.prevent.stop="login()"
                        :disabled="username && password ? false : true"
                    >Login</button>
                    <router-link to="/signup" class="signup-button clear button">Sign up</router-link>
                </form>
                <p
                    v-for="msg in errors['non_field_errors']"
                    class="error-message"
                >{{ msg }}</p>
            </div>
        </div>
    </div>
</template>

<script>
 export default {
     data: function() {
         return {
             username: null,
             password: null,
             errors: {}
         }
     },
     methods: {
         login() {
             // don't do anything if we don't have a username and password
             if (!this.$data.username || !this.$data.password) return;

             this.$http.post('/api/auth/login/', {
                 username: this.$data.username,
                 password: this.$data.password
             })
                 .then((response) => {
                     return response.json().then((data) => [response, data])
                 })
                 .then((response_data) => {
                     const [response, data] = response_data
                     this.$store.commit('setToken', data.token)
                     this.$store.commit('setCurrentUser', data.user)
                     this.$router.replace('/')
                 })
                 .catch((err) => {
                     console.log(err)
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
 .login-container {
     margin-top: 20px;
 }

 input[name=password] {
     margin-bottom: 0;
 }

 .forgot-password-link {
     display: block;
     font-size: 12px;
     width: 100%;
     text-align: right;
 }

 .login-button {
     margin-top: 28px;
 }

 .button {
     width: 100%;
 }

 .error-message {
     color: red;
 }
</style>
