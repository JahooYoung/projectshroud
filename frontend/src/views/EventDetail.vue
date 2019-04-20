<template>
  <div>
    <b-spinner v-if="pageSwitch === 0" style="width: 3rem; height: 3rem;" label="Loading..."></b-spinner>

    <EventDetailAdmin v-if="pageSwitch === 2"/>

    <div v-if="pageSwitch === 1">
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


      <b-button variant="primary" v-show="!event.registered" v-b-modal.modal-register>
        <b-spinner small type="grow" v-show="isLoading"></b-spinner>
        Register
      </b-button>

      <b-modal
        id="modal-register"
        ref="modal1"
        title="Register infomation"
        @ok="register"
      >
        <!-- Modal Component  @click="register" -->
        
        <form @submit.stop.prevent="empty_check" label="Your Name">
          <b-form-input v-model="name" placeholder="Enter your name"></b-form-input>
        </form>
        <p> </p>
        <div>
          <b-form-group label="Transport ways">
            <b-form-radio v-model="selected" value="plane">Plane</b-form-radio>
            <b-form-radio v-model="selected" value="train">Train</b-form-radio>
            <b-form-radio v-model="selected" value="others">Others</b-form-radio>
          </b-form-group>
        </div>

      </b-modal>
      

      <b-button variant="danger" v-show="event.registered" v-b-modal.modal-unregister>
        <b-spinner small type="grow" v-show="isLoading"></b-spinner>
        Unregister
      </b-button>
      <b-modal id="modal-unregister" ref="modal2" title="Notice" @ok="unregister">
        <p class="my-4">Are you sure to unregister?</p>
      </b-modal>

      <h4> {{status}} </h4>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import EventDetailAdmin from './EventDetailAdmin/Entry'

function date2input (date) {
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  date.setSeconds(0, 0)
  date = date.toISOString()
  return date.substr(0, date.length - 1)
}

export default {
  computed: mapState({
    user: 'user'
  }),
  data () {
    return {
      pageSwitch: 0, // 0: first time loading, 1: normal, 2: admin
      isLoading: false,
      event: {
        title: '',
        description: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        registered: false,
        requireApprove: false
      },
      name: '',
      status: '',
      selected: false
    }
  },
  mounted () {
    this.isLoading = true
    this.axios.get('/api/event/' + this.$route.params.id)
      .then(res => {
        console.log(res.data)
        this.isLoading = false
        if (res.data.event_admin) {
          this.pageSwitch = 2
        } else {
          this.event.title = res.data.title
          this.event.description = res.data.description
          this.event.startTime = date2input(new Date(res.data.start_time))
          this.event.endTime = date2input(new Date(res.data.end_time))
          this.event.location = res.data.location
          this.event.public = res.data.public
          this.event.registered = res.data.event_registered
          this.event.requireApprove = res.data.require_approve
          this.pageSwitch = 1
        }
      })
      .catch(err => {
        this.isLoading = false
        console.log('failed to fetch events\n', err)
      })
  },
  methods: {
    empty_check() {

    },
    register () {
      this.status = 'Registering...'
      this.isLoading = true
      console.log('Trying to register')
      if (this.user === null) {
        this.isLoading = false
        this.status = 'Please login first'
      } else {
        console.log('id=' + this.$route.params.id)
        this.axios.post('/api/register/', {
          event_id: this.$route.params.id
        })
          .then(res => {
            this.isLoading = false
            console.log(res.data)
            console.log("selected = " + this.selected);
            if (res.status === 201) {
              this.status = 'Register successfully'
              this.event.registered = true
            } else {
              alert(res.data)
              this.status = null;
            }
          })
          .catch(err => {
            this.isLoading = false
            this.status = 'Fail to register'
            console.log(err)
          })
      }
    },
    unregister () {
      this.status = 'Unregistering...'
      this.isLoading = true
      console.log('Trying to unregister')
      if (this.user === null) {
        this.isLoading = false
        this.status = 'Please login first'
      } else {
        console.log('id=' + this.$route.params.id)
        this.axios.post('/api/unregister/', {
          event_id: this.$route.params.id
        })
          .then(res => {
            this.isLoading = false
            console.log(res.data)
            if (res.status === 200) {
              this.status = 'Unregister successfully'
              this.event.registered = false
            } else {
              alert(res.data)
              this.status = null;
            }
          })
          .catch(err => {
            this.isLoading = false
            this.status = 'Fail to unregister'
            console.log(err)
          })
      }
    }
  },
  components: {
    EventDetailAdmin
  }
}
</script>
