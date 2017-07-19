<template>
    <div class="job-form-container grid-container">
        <div class="grid-x">
            <div class="medium-8 medium-offset-2 cell">
                <form id="jog-form">
                    <label>Date
                        <input type="text" name="date" ref="jogDateInput"/>
                        <inline-errors :errors="errors['date']"></inline-errors>
                    </label>
                    <label>Distance
                        <div class="input-group">
                            <input class="input-group-field" type="number"
                                   name="distance_in_feet" v-model="distanceInFeet"/>
                            <span class="input-group-label">ft.</span>
                        </div>
                        <inline-errors :errors="errors['distance_in_feet']"></inline-errors>
                    </label>

                    <label>Duration
                        <div class="input-group">
                            <input class="input-group-field" type="number" name="time_in_seconds"
                                   v-model="timeInSeconds"/>
                            <span class="input-group-label">minutes</span>
                        </div>
                        <inline-errors :errors="errors['time_in_seconds']"></inline-errors>
                    </label>

                    <div class="actions grid-x align-justify" v-if="!confirmDelete">
                        <div class="cell small-4">
                            <a v-if="jogId" class="alert clear button" @click="confirmDelete=true">Delete</a>
                        </div>
                        <div class="text-right cell small-6">
                            <a class="clear button" @click="cancel()">Cancel</a>
                            <a class="button" @click="save()">Save</a>
                        </div>
                    </div>

                    <div class="confirm-delete-container grid-x align-justify" v-if="confirmDelete">
                        <p class="cell small-6">Are you sure you want to delete this jog?</p>
                        <div class="text-right cell small-6">
                            <a class="clear button" @click="confirmDelete=false">No</a>
                            <a class="delete-yes-button alert button" @click="remove()">Yes</a>
                        </div>
                    </div>
                </form>

                <inline-errors :errors="errors['non_field_errors']"></inline-errors>
            </div>
        </div>
    </div>
</template>

<script>
 import VueRouter from 'vue-router'
 import Pikaday from 'pikaday'
 import moment from 'moment'
 import toastr from 'toastr'

 export default {
     data: function() {
         return {
             jogId: null,
             date: null,
             timeInSeconds: null,
             distanceInFeet: null,
             errors: { },
             confirmDelete: false
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
             this.$http.get(`/api/jogs/${this.$data.jogId}/`)
                 .then((response) => {
                     if (!response.ok) {
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
             let method = 'post'
             let url = '/api/jogs/'
             if (this.$data.jogId) {
                 method = 'put'
                 url = `${url}${this.$data.jogId}/`
             }
             this.$http[method](url, {
                 date: formattedDate,
                 distance_in_feet: this.$data.distanceInFeet,
                 time_in_seconds: this.$data.timeInSeconds
             }).then((response) => {
                 return response.json().then(data => [response, data])
             }).then((response_data) => {
                 const [response, data] = response_data
                 if (!response.ok) {
                     this.$data.errors = data
                     return
                 }

                 toastr.success('Jog saved')

                 this.$store.commit('addJog', data)
                 this.$router.back(); // pop router history
             }).catch((err) => {
                 console.log(err)
                 const contentType = err.headers ? err.headers.map['Content-Type'] : []
                 if (contentType.includes('application/json')) {
                     err.json().then((data) => this.$data.errors = data)
                 } else {
                     this.$set(this.$data.errors, 'non_field_errors', ['Unknown error'])
                 }
             })
         },

         remove() {
             const jogId = this.$data.jogId
             this.$http.delete(`/api/jogs/${jogId}/`)
                 .then((response) => {
                     if (!response.ok) {
                         /* this.$data.errors = response.body*/
                         console.error(response.body)
                         return;
                     }

                     toastr.success('Jog deleted')
                     this.$store.commit('deleteJog', jogId)
                     this.$router.back(); // pop router history
                 }).catch((err) => {
                     console.error(err)
                     this.$data.errors = { 'non_field_errors': ['Unknown error'] }
                 })
                 .then(() => this.confirmDelete = false)
         }
     }
 }
</script>

<style lang="scss" scoped>
 .confirm-delete-container {
     padding: 10px;
     margin: 10px 0;
     background: #cc4b37;
     color: white;

     .button {
         color: white;
     }
 }

 .delete-yes-button {
     border: solid 1px white;
 }
</style>
