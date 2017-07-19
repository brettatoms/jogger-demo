<template>
    <div class="job-form-container grid-container">
        <div class="grid-x">
            <div class="medium-8 medium-offset-2 cell">
                <form id="jog-form">
                    <label>Date
                        <input type="text" name="date" ref="jogDateInput"/>
                        <p
                            v-for="msg in errors['date']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>
                    <label>Distance
                        <div class="input-group">
                            <input class="input-group-field" type="number"
                                   name="distance_in_feet" v-model="distanceInFeet"/>
                            <span class="input-group-label">ft.</span>
                        </div>
                        <p
                            v-for="msg in errors['distance_in_feet']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>

                    <label>Duration
                        <div class="input-group">
                            <input class="input-group-field" type="number" name="time_in_seconds"
                                   v-model="timeInSeconds"/>
                            <span class="input-group-label">minutes</span>
                        </div>
                        <p
                            v-for="msg in errors['time_in_seconds']"
                            class="error-message help-text"
                        >{{ msg }}</p>
                    </label>

                    <a class="cancel-button clear button" @click="cancel()">Cancel</a>
                    <a class="login-button button" @click="save()">Save</a>
                </form>
                <p
                    v-for="msg in errors['non_field_errors']"
                    class="error-message"
                >{{ msg }}</p>
            </div>
        </div>
    </div>
</template>

<script>
 import VueRouter from 'vue-router'
 import Pikaday from 'pikaday'
 import moment from 'moment'

 export default {
     data: function() {
         return {
             jogId: null,
             date: null,
             timeInSeconds: null,
             distanceInFeet: null,
             errors: { }
         }
     },

     mounted() {
         this._jogDatePicker = new Pikaday({
             field: this.$refs.jogDateInput,
             format: 'YYYY-MM-DD',
             onSelect: (date) => {
                 this.$data.date = date
             }
         })
     },
     created() {
         this.$data.jogId = this.$route.query.id
         if (this.$data.jogId) {
             // get jog details
             fetch(`/api/jogs/${this.$data.jogId}/`, {
                 headers: {
                     'Authorization': `Token ${this.$store.state.token}`,
                 }
             }).then((response) => {
                 if (response.status !== 200) {
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                     return;
                 }

                 return response.json().then((data) => {
                     this.$data.jogId = data.id
                     this.$data.timeInSeconds = data.time_in_seconds
                     this.$data.distanceInFeet = data.distance_in_feet
                     this.$data.date = data.date
                     this._jogDatePicker.setDate(data.date)
                 })
             }).catch((err) => {
                 console.log(err)
                 this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
             })
         }
     },

     methods: {
         cancel() {
             this.$router.back()
         },
         save() {
             const date = this.$data.date;
             const formattedDate  = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
             let method = 'POST'
             let url = '/api/jogs/'
             if (this.$data.jogId) {
                 method = 'PUT'
                 url = `${url}${this.$data.jogId}/`
             }
             fetch(url, {
                 method,
                 body: JSON.stringify({
                     date: formattedDate,
                     distance_in_feet: this.$data.distanceInFeet,
                     time_in_seconds: this.$data.timeInSeconds
                 }),
                 headers: {
                     'Authorization': `Token ${this.$store.state.token}`,
                     'Content-Type': 'application/json'
                 }
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 if (response.status !== 200) {
                     this.$data.errors = data
                 } else {
                     this.$store.commit('addJog', data)
                     this.$router.back(); // pop router history
                 }
             }).catch((err) => {
                 this.$data.errors = { 'non_field_errors': ['Unknown error'] }
             })
         }
     }
 }
</script>

<style lang="scss" scoped>
 .error-message {
     color: red;
 }
</style>
