<template>
    <div>
        <router-link to="/add">Add Jog</router-link>
        <table class="jog-table">
            <thead>
                <tr>
                    <th><a @click="sortBy('date')">Date</a></th>
                    <th><a @click="sortBy('distance')">Distance</a></th>
                    <th><a @click="sortBy('time')">Time</a></th>
                </tr>
            </thead>
            <tr class="jog-row"v-for="jog in formattedJogs">
                <td>{{ jog.date }}</td>
                <td>{{ jog.distance_in_feet }}</td>
                <td>{{ jog.time_in_seconds }}</td>
            </tr>
        </table>
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
         const token = localStorage.getItem('token')
         if (!token) {
             return this.$router.replace('/login')
         }

         this.loadJogs();
     },

     computed: {
         formattedJogs() {
             const direction = this.sortAsc ? ['asc', 'asc'] : ['desc', 'desc']

             // use the sort key and the id so the sort is stable
             return orderBy(this.$store.state.jogs, (jog) => {
                 return this.sortKey === 'date' ?
                        new moment(jog.date, 'YYYY-MM-DD').valueOf() :
                        jog[this.sortKey]
             }, direction)
                 .map((jog) => {
                     return {
                         date: moment(jog.date).format('MMM, M, YYYY'),
                         distance_in_feet: jog.distance_in_feet,
                         time_in_seconds: jog.time_in_seconds
                     }

                 })
         }
     },

     methods: {
         sortBy(key) {
             const sortKey = {
                 date: 'date',
                 distance: 'distance_in_feet',
                 time: 'time_in_seconds'
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
             const token = localStorage.getItem('token')
             fetch('/api/jogs/', {
                 headers: {
                     'Authorization': `Token ${token}`
                 }
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 this.$store.state.jogs = data
             }).catch((err) => {
                 // TODO: handle error
             })
         }
     }
 }
</script>

<style lang="scss" scoped>
 .jog-table {
     margin-top: 12px;
     width: 100%;

     th {
         text-align: left;
     }
 }
</style>
