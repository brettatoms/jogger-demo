import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import 'whatwg-fetch'

import App from './app.vue'
import Login from './login.vue'
import Signup from './signup.vue'
import Jogs from './jogs.vue'
import JogForm from './jog-form.vue'

Vue.use(VueRouter)
Vue.use(Vuex)

const routes = [
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/', component: Jogs },
    { path: '/edit', component: JogForm },
    { path: '/add', component: JogForm }
]

const router = new VueRouter({ routes })

const store = new Vuex.Store({
    state: {
        jogs: [],
        toasts: []
    },
    mutations: {
        addJog(state, jog) {
            state.jogs.unshift(jog)
        }
    }
})

new Vue({
    router,
    components: { App },
    store
}).$mount('#root')
