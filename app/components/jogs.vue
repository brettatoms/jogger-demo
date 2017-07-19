<template>
    <div>
        <router-link class="clear button" to="/add" v-if="formattedJogs.length">Add Jog</router-link>
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
        <div class="empty-state" v-if="!formattedJogs.length">
            <router-link to="/add" class="button">Add Jog</router-link>
        </div>
    </div>
</template>

<script>
 import moment from 'moment';
 import VueRouter from 'vue-router'
 import orderBy from 'lodash.orderby'

 export default {
     data: function() {
         return {
             sortKey:  'date',
             sortAsc: true,
         }
     },
     beforeMount() {
         this.loadJogs();
     },

     computed: {
         formattedJogs() {
             const formattedData = this.$store.state.jogs
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

         loadJogs() {
             this.$http.get('/api/jogs/')
                 .then((response) => {
                     return response
                         .json()
                         .then((data) => {
                             this.$store.commit('setJogs', response.body)
                     })
                 }).catch((err) => {
                     if (err.json) {
                         err.json().then((data) => this.$data.errors = data)
                     } else {
                         this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
                     }
                 })
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
</style>
