<template>
    <div>
        <div v-if="isOtherUser" class="callout small text-center warning">
            You are currently viewing the jogs for <b>{{ otherUser.username }}</b>
        </div>

        <div v-if="formattedJogs.length || fromDate || toDate">
            <div class="grid-x grid-padding-x">
                <div class="auto cell">
                    <router-link class="clear button" to="/add">Add Jog</router-link>
                </div>
                <div class="medium-3 cell">
                    <label class="from-label">From
                        <input type="text" name="fromDate" ref="fromDateInput"/>
                        <p class="help-text"><a @click.prevent="clearFromDate()">clear</a></p>
                    </label>
                </div>
                <div class="medium-3 cell">
                    <label class="to-label">To
                        <input type="text" name="toDate" ref="toDateInput"/>
                        <p class="help-text"><a @click.prevent="clearToDate()">clear</a></p>
                    </label>
                </div>
            </div>
        </div>

        <inline-errors :errors="[errors.detail]"></inline-errors>

        <table class="jog-table" v-if="formattedJogs.length">
            <thead>
                <tr>
                    <th><a @click="sortBy('date')">Date</a></th>
                    <th><a @click="sortBy('distance')">Distance (feet)</a></th>
                    <th><a @click="sortBy('time')">Time (minutes)</a></th>
                    <th><a @click="sortBy('speed')">Avg Speed (mph)</a></th>
                </tr>
            </thead>
            <tbody>
                <tr class="jog-row" v-for="jog in formattedJogs" @click="editJog(jog)">
                    <td>{{ jog.date }}</td>
                    <td>{{ jog.distanceInFeet }}</td>
                    <td>{{ jog.timeInMinutes }}</td>
                    <td>{{ jog.averageSpeed }}</td>
                </tr>
            </tbody>
        </table>
        <div class="empty-state" v-if="!formattedJogs.length && !fromDate && !toDate">
            <router-link to="/add" class="button">Add Jog</router-link>
        </div>
    </div>
</template>

<script>
 import moment from 'moment';
 import VueRouter from 'vue-router'
 import orderBy from 'lodash.orderby'
 import Pikaday from 'pikaday'
 import { handleErrorResponse } from './utils'

 export default {
     data: function() {
         return {
             sortKey:  'date',
             sortAsc: true,
             fromDate: null,
             toDate: null,
             jogs: [],
             errors: { }
         }
     },

     beforeMount() {
         const userId = this.$route.query.user_id

         // if we already have jogs in the store then start with those
         if (this.$store.state.jogs.length) {
             this.$data.jogs = this.$store.state.jogs
         }

         this.loadJogs(userId)
             .then((jogs) => {
                 if (!userId) {
                     this.$store.commit('setJogs', jogs)
                     this.$data.jogs = this.$store.state.jogs
                 } else {
                     this.$data.jogs = jogs
                 }
             })
            .catch((err) => console.error(err))

     },

     mounted() {
         // TODO: we should watch for the date inputs to be available
         // before we init pikaday
         this._fromDatePicker = new Pikaday({
             field: this.$refs.fromDateInput,
             format: 'YYYY-MM-DD',
             onSelect: (date) => {
                 this.$data.fromDate = date
             }
         })

         this._toDatePicker = new Pikaday({
             field: this.$refs.toDateInput,
             format: 'YYYY-MM-DD',
             onSelect: (date) => {
                 this.$data.toDate = date
             }
         })
     },

     computed: {
         isOtherUser() {
             return this.$route.query.user_id && this.$route.query.user_id !== this.$store.state.currentUser.id
         },

         otherUser() {
             if (!this.$route.query.user_id) {
                 return
             }

             return this.$store.state.users.find((u) => u.id == this.$route.query.user_id)

         },

         formattedJogs() {
             if (!this.$data.jogs) return []

             const filteredData = this.$data.jogs
                 .filter((jog) => {
                     // filter out days before fromDate
                     const { fromDate, toDate } = this.$data;
                     if (fromDate && moment(jog.date).isBefore(fromDate, 'day')) {
                         return false
                     }
                     // filter out days after toDate
                     if (toDate && moment(jog.date).isAfter(toDate, 'day')) {
                         return false
                     }

                     return true;
                 })

             const formattedData = filteredData
                 .map((jog) => {
                     const averageSpeed = ((jog.distance_in_feet / 5280 ) / (jog.time_in_seconds))
                     return {
                         id: jog.id,
                         date: moment(jog.date, 'YYYY-MM-DD').format('MMM D, YYYY'),
                         distanceInFeet: jog.distance_in_feet,
                         timeInMinutes: jog.time_in_seconds * 60,
                         averageSpeed: averageSpeed.toFixed(2)
                     }
                 })

             const direction = this.sortAsc ? ['asc', 'asc'] : ['desc', 'desc']
             return orderBy(formattedData, (jog) => {
                 return this.sortKey === 'date' ?
                        new moment(jog.date, 'YYYY-MM-DD').valueOf() :
                        jog[this.sortKey]
             }, direction)
         }
     },

     methods: {
         clearFromDate() {
             this.$data.fromDate = null
             this._fromDatePicker.setDate(null)
         },
         clearToDate() {
             this.$data.toDate = null
             this._toDatePicker.setDate(null)
         },
         sortBy(key) {
             const sortKey = {
                 date: 'date',
                 distance: 'distanceInFeet',
                 time: 'timeInMinutes',
                 speed: 'averageSpeed'
             }[key];

             // reverse the sort order if we're already sorting by this key
             if (this.sortKey === sortKey) {
                 this.sortAsc = !this.sortAsc
             } else {
                 this.sortKey = sortKey
                 this.sortAsc = true
             }
         },

         loadJogs(userId) {
             const url = userId ? `/api/users/${userId}/jogs/` : '/api/jogs/'
             return this.$http.get(url)
                 .then((response) => response.json())
                 .catch((err) => handleErrorResponse(this, err))
         },

         editJog(jog) {
             this.$router.push({
                 path: '/edit',
                 query: { id: jog.id }
             })
         }
     }
 }
</script>

<style lang="scss" scoped>
 .jog-table {
     width: 100%;


     th, td {
         text-align: left;
         padding-left: 10px;
     }

     tbody {
         tr {
             &:hover {
                 text-decoration: underline;
                 cursor: pointer;
                 background: #eee;
             }
         }
     }
 }

 .empty-state {
     text-align: center;
     margin: 20px;
 }

 .from-label,
 .to-label {
     input {
         margin-bottom: 4px;
     }
 }

 .warning {
     background:  #fff3d9;
 }
</style>
