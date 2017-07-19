<template>
    <table>
        <thead>
            <th>Week</th>
            <th>Total jogs</th>
            <th>Total distance</th>
            <th>Avg distance</th>
            <th>Avg. speed</th>
        </thead>
        <tbody>
            <tr v-for="row in formattedData">
                <td>{{ row.startOfWeek }}</td>
                <td>{{ row.numJogs }}</td>
                <td>{{ row.totalDistance }} ft.</td>
                <td>{{ row.averageDistance }} ft.</td>
                <td>{{ row.averageSpeed }} mph</td>
            </tr>
        </tbody>
    </table>
</template>
<script>
 import get from 'lodash.get'
 import moment from 'moment';

 export default {
     computed: {
         formattedData() {
             const totals = this.$store.state.jogs.reduce((groups, jog) => {
                 const startOfWeek = moment(jog.date).startOf('week').format('YYYY-MM-DD')
                 groups[startOfWeek] = {
                     timeInSeconds: get(groups, `${startOfWeek}.timeInSeconds`, 0) + jog.time_in_seconds,
                     distanceInFeet: get(groups, `${startOfWeek}.distanceInFeet`, 0) + jog.distance_in_feet,
                     numJogs: get(groups, `${startOfWeek}.numJogs`, 0) + 1
                 }
                 return groups
             }, {})

             const sortedWeeks = Object.keys(totals).sort()

             const weeklyAverages = sortedWeeks.map((startOfWeek) => {
                 const { numJogs, distanceInFeet, timeInSeconds } = totals[startOfWeek]
                 const averageSpeed = ((distanceInFeet / 5280) / timeInSeconds)
                 return {
                     startOfWeek,
                     numJogs: numJogs,
                     totalDistance: distanceInFeet,
                     averageDistance: Math.round(distanceInFeet / numJogs),
                     averageSpeed: averageSpeed.toFixed(2),
                 }
             })

             return weeklyAverages
         }
     }
 }
</script>
<style lang="scss" scoped>
 table {
     width: 100%;

     th, td {
         text-align: left;
         padding-left: 10px;
     }
 }
</style>
