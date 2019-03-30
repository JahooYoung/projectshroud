<template>
  <div>
    <EventDetailAdmin v-if="isAdmin"/>
    <div v-if="!isAdmin">
      <!-- fill this in -->
      <h2> {{event.title}} </h2>
      <h4> location: {{event.location}} </h4>
      <h4> start time: {{event.startTime}} </h4>
      <h4> end time: {{event.endTime}} </h4>
      
      <h4> Descripition: </h4>
      <b-container class="bv-example-row">
        <b-row class="justify-content-md-center">
          <b-col cols="8">
          {{event.description}}
          <!--<b-alert variant="success" show></b-alert>-->
          </b-col>
        </b-row>
      </b-container>
      
      <b-button variant="primary" type="submit" :disable="isLoading" @click="register">
        <b-spinner small type="grow" v-show="isLoading"></b-spinner>
        Register
      </b-button>
    </div>
  </div>
</template>

<script>
import EventDetailAdmin from './EventDetailAdmin/Entry'

function date2input (date) {
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  date.setSeconds(0, 0)
  date = date.toISOString()
  return date.substr(0, date.length - 1)
}

function input2date (str) {
  let date = new Date(str)
  return date
}

export default {
  data () {
    return {
      isLoading: false,
      isAdmin: false,
      event: {
        title: '',
        description: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        requireApprove: false
      },
    }
  },
  
  mounted() {
    this.isLoading = true
      this.axios.get('/api/event/' + this.$route.params.id)
        .then(res => {
          this.isLoading = false
          console.log(res.data)
          this.event.title = res.data.title
          this.event.description = res.data.description
          this.event.startTime = date2input(new Date(res.data.start_time))
          this.event.endTime = date2input(new Date(res.data.end_time))
          this.event.location = res.data.location
          this.event.public = res.data.public
          this.event.requireApprove = res.data.require_approve
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to fetch events\n', err)
        })
  },
  methods: {
    register () {
      this.isLoading = true
      console.log('Trying to register')
      console.log()
      setTimeout(err => {
        this.isLoading = false
      }, 1000);
    },
  },
  components: {
    EventDetailAdmin
  }
}
</script>
