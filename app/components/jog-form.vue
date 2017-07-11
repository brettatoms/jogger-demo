<template>
    <div class="job-form-container grid-container">
        <div class="grid-x">
            <div class="medium-8 medium-offset-2 cell">
                <form id="jog-form">
                    <label>Date
                        <input type="text" name="date" ref="jogDateInput" />
                    </label>
                    <label>Distance
                        <div class="input-group">
                            <input class="input-group-field" type="number"
                                   name="distance_in_feet" v-model="distanceInFeet"/>
                            <span class="input-group-label">ft.</span>
                        </div>
                    </label>

                    <label>Duration
                        <div class="input-group">
                            <input class="input-group-field" type="number" name="time_in_seconds"
                                   v-model="timeInSeconds"/>
                            <span class="input-group-label">minutes</span>
                        </div>
                    </label>

                    <a class="cancel-button clear button" @click="cancel()">Cancel</a>
                    <a class="login-button button" @click="save()">Save</a>
                </form>

            </div>
        </div>
    </div>
</template>

<script>
 import VueRouter from 'vue-router'
 import Pikaday from 'pikaday'

 export default {
    data: function() {
         return {
             date: null,
             timeInSeconds: null,
             distanceInFeet: null
         }
     },

    mounted() {
        this._jogDatePicker = new Pikaday({
            field: this.$refs.jogDateInput,
            onSelect: (date) => {
                this.$data.date = date
            }
        })
    },

     methods: {
         cancel() {
             this.$router.back()
         },
         save() {
             const token = localStorage.getItem('token')
             const date = this.$data.date;
             const formattedDate  = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
             fetch('/api/jogs/', {
                 method: 'POST',
                 body: JSON.stringify({
                     date: formattedDate,
                     distance_in_feet: this.$data.distanceInFeet,
                     time_in_seconds: this.$data.timeInSeconds
                 }),
                 headers: {
                     'Authorization': `Token ${token}`,
                     'Content-Type': 'application/json'
                 }
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 this.$store.commit('addJog', data)
                 this.$router.back(); // pop router history
             }).catch((err) => {
                 // TODO: handle error
                 console.log(err)
             })

         }
     }
 }
</script>

<style>
</style>
