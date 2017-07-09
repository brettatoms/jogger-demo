<template>
    <div class="login-container grid-container">
        <div class="grid-x">
            <div class="small-4 small-offset-4 cell">
                <div class="card">
                    <form id="login-form" @keyup.13="login()">
                        <label>Username
                            <input type="text" name="username" />
                        </label>
                        <label>Password
                            <input type="password" name="password" />
                        </label>

                        <a class="login-button button" @click="login()">Login</a>
                        <router-link to="/signup " class="signup-button clear button">Sign up</router-link>
                    </form>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
 export default {
     methods: {
         login() {
             var form = new FormData(document.getElementById('login-form'));
             fetch('/api/auth/login/', {
                 method: 'POST',
                 body: form
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 console.log(`data: ${data}`)
                 if (response.status === 200) {
                     localStorage.setItem('token', data['key'])
                     this.$router.replace('/')
                 } else {
                     // TODO: handle error
                 }
             }).catch((err) => {
                 // TODO: handle error
             })
         }
     }
 }
</script>

<style>
 .login-container {
     margin-top: 100px;
 }

 .button {
     width: 100%;
 }
</style>
