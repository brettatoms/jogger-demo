import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import VueResource from 'vue-resource'
import createPersistedState from 'vuex-persistedstate'
import toastr from 'toastr'

import App from './app.vue'
import Login from './login.vue'
import Signup from './signup.vue'
import Jogs from './jogs.vue'
import JogForm from './jog-form.vue'
import Users from './users.vue'
import UserForm from './user-form.vue'
import InlineErrors from './inline-errors.vue'
import WeeklyReport from './weekly-report.vue'
import TopBar from './top-bar.vue'
import SideBar from './side-bar.vue'

Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueResource)

// register global components
Vue.component('inline-errors', InlineErrors)
Vue.component('top-bar', TopBar)
Vue.component('side-bar', SideBar)

toastr.options.closeButton = true
toastr.options.positionClass = 'toast-top-center'

const routes = [
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/', component: Jogs },
    { path: '/edit', component: JogForm },
    { path: '/add', component: JogForm },
    { path: '/users', component: Users },
    { path: '/users/add', component: UserForm },
    { path: '/users/edit', component: UserForm },
    { path: '/report', component: WeeklyReport }
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
            state.users = []
            state.currentUser = null
            state.jogs =[]
        },
        setJogs(state, jogs) {
            state.jogs = jogs
        },
        addJog(state, jog) {
            state.jogs.unshift(jog)
        },
        deleteJog(state, jog) {
            const index = state.jogs.findIndex((j) => j.id == jog.id)
            if (index !== -1) {
                state.jogs.splice(index, 1)
            }
        },
        addUser(state, user) {
            state.users.unshift(user)
        },
        updateUser(state, user) {
            const existingUser = state.users.find((u) => u.id == user.id)
            if (existingUser) {
                Object.assign(existingUser, user)
            } else {
                state.users.unshift(user)
            }

            // also update the current user
            if (user.id === state.currentUser.id) {
                Object.assign(state.currentUser, user)
            }
        },
        setUsers(state, users) {
            state.users = users
        },
        deleteUser(state, userId) {
            if (userId == state.currentUser.id) {
                state.commit('logout')
                return
            }

            const index = state.users.findIndex((u) => u.id == userId)
            if (index !== -1) {
                state.users.splice(index, 1)
            }
        }
    }
})

Vue.http.interceptors.push(function(request, next) {
    // set the authorization token if there is one in the store
    if (store.state.token) {
        request.headers.set('Authorization', `Token ${this.$store.state.token}`)
    }

    // continue to next interceptor
    next((response) => {
        // if the request is unauthorized then redirect to login
        if (response.status == 401) {
            store.commit('logout')
            router.replace('/login')
        }
    });
});

new Vue({
    router,
    components: { App },
    store,
    http: {
        root: '/api',
    }
}).$mount('#root')
