<template>
    <div class="signup-container grid-container">
        <div class="grid-x">
            <div class="small-10 small-offset-1 cell">
                <form id="signup-form" @keyup.13="signup()">
                    <label>Username
                        <input type="text" name="username" v-model="username"/>
                        <p
                            v-for="msg in errors['username']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>
                    <label>Password
                        <input type="password" name="password1" v-model="password1"/>
                        <p
                            v-for="msg in errors['password1']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>

                    <label>Confirm Password
                        <input type="password" name="password2" v-model="password2"/>
                        <p
                            v-for="msg in errors['password2']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>

                    <button
                        class="signup-button button"
                        type="button"
                        @click="signup()"
                        :disabled="username && password1 && password2 ? false : true"
                    >Signup</button>
                    <router-link to="/login" class="login-button clear button">Login</router-link>
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
             password1: null,
             password2: null,
             errors: {}
         }
     },
     methods: {
         signup() {
             // don't do anything if we don't have a username and password
             if (!this.$data.username || !this.$data.password1 || !this.$data.password2) return;

             var form = new FormData(document.getElementById('signup-form'));
             fetch('/api/auth/register', {
                 method: 'POST',
                 body: form
             }).then((response) => {
                 return response.json().then((data) => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 if (response.status === 201) {
                     localStorage.setItem('token', data['key'])
                     this.$router.replace('/')
                 } else {
                     this.$data.errors = data;
                 }
             }).catch((err) => {
                 this.$data.errors['non_field_errors'] = 'Unknown error'
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
