import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import VueResource from 'vue-resource'
import createPersistedState from 'vuex-persistedstate'
import 'whatwg-fetch'

import App from './app.vue'
import Login from './login.vue'
import Signup from './signup.vue'
import Jogs from './jogs.vue'
import JogForm from './jog-form.vue'
import Users from './users.vue'
import UserForm from './user-form.vue'
import InlineErrors from './inline-errors.vue'

Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueResource)

// register global components
Vue.component('inline-errors', InlineErrors)

const routes = [
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/', component: Jogs },
    { path: '/edit', component: JogForm },
    { path: '/add', component: JogForm },
    { path: '/users', component: Users },
    { path: '/users/add', component: UserForm },
    { path: '/users/edit', component: UserForm }
]

const router = new VueRouter({ routes })

router.beforeEach((to, from, next) => {
    // redirect to login if we don't have a login token
    const non_auth_routes = new Set(['/login', '/signup'])
    if (store.state.token || non_auth_routes.has(to.path)) {
        next()
    } else {
        next('/login')
    }
})

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        // username: null,
        currentUser: null,
        token: null,
        jogs: [],
        users: []
    },
    mutations: {
        setCurrentUser(state, user) {
            state.currentUser = user
        },
        setToken(state, token) {
            state.token = token
        },
        logout(state) {
            state.token = null
        },

        setJogs(state, jogs) {
            state.jogs = jogs
        },
        addJog(state, jog) {
            state.jogs.unshift(jog)
        },

        addUser(state, user) {
            state.users.unshift(user)
        },
        updateUser(state, user) {
            const existingUser = state.users.find((u) => u.user_id == user.user_id)
            if (existingUser) {
                Object.assign(existingUser, user)
            } else {
                state.users.unshift(user)
            }
        },
        setUsers(state, users) {
            state.users = users
        }
    }
})

Vue.http.interceptors.push(function(request, next) {
    // set the authorization token if there is one in the store
    if (store.state.token) {
        request.headers.set('Authorization', `Token ${this.$store.state.token}`)
    }

    // continue to next interceptor
    next();
});

new Vue({
    router,
    components: { App },
    store,
    http: {
        root: '/api',
    }
}).$mount('#root')
