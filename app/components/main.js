import Vue from 'vue'
import VueRouter from 'vue-router'
import 'whatwg-fetch'

import App from './app.vue'
import Login from './login.vue'
import Signup from './signup.vue'
import Jogs from './jogs.vue'

Vue.use(VueRouter)

const routes = [
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/', component: Jogs }
]

const router = new VueRouter({ routes })

new Vue({
    router,
    components: { App }
}).$mount('#root')
