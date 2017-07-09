<template>
    <div class="signup-container grid-container">
        <div class="grid-x">
            <div class="small-4 small-offset-4 cell">
                <div class="card">
                    <form id="signup-form" @keyup.13="signup()">
                        <label>Username
                            <input type="text" name="username" />
                        </label>
                        <label>Password
                            <input type="password" name="password1" />
                        </label>
                        <label>Confirm Password
                            <input type="password" name="password2" />
                        </label>

                        <a class="signup-button button" @click="signup()">Signup</a>
                        <router-link to="/login" class="login-button clear button">Login</router-link>
                    </form>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
 export default {
     methods: {
         signup() {
             console.log('signup()')
             var form = new FormData(document.getElementById('signup-form'));
             fetch('/api/auth/register', {
                 method: 'POST',
                 body: form
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 console.log(`data: ${data}`)
                 if (response.status === 201) {
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
 .signup-container {
     margin-top: 100px;
 }

 .button {
     width: 100%;
 }
</style>
