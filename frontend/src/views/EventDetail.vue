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
          <!--<b-alert variant="success" show></b-alert>     @click="register"@click="unregister"-->
          </b-col>
        </b-row>
      </b-container>
      <b-button v-b-modal.modal-register variant="primary" type="submit" :disabled="isLoading" v-show="!event.registered">
        <b-spinner small type="grow" v-show="isLoading"></b-spinner>
        Register
      </b-button>

      <b-button v-b-modal.modal-unregister variant="danger" type="submit" :disabled="isLoading" v-show="event.registered">
        <b-spinner small type="grow" v-show="isLoading"></b-spinner>
        Unregister
      </b-button>
      <b-modal id="modal-register" @ok="register" title="Basic infomation">

        <b-form-group label="Your Name:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="attendee.name"
            placeholder="Enter name"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Your transport type:" label-for="input-2">
          <b-form-select
            id="input-2"
            v-model="attendee.transport_type"
            :options="transport_options">
          </b-form-select>
        </b-form-group>

        <b-form-group label="Your transport id:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="attendee.transport_id"
            placeholder="Enter transport id"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Your depart station:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="attendee.depart_station"
            placeholder="Enter depart station"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Your depart_time:" label-for="input-5">
          <b-form-input
            type="datetime-local"
            id="input-5"
            v-model="attendee.depart_time"
            placeholder="Enter depart time"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Your arrival_station:" label-for="input-6">
          <b-form-input
            id="input-6"
            v-model="attendee.arrival_station"
            placeholder="Enter arrival station"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Your arrival time:" label-for="input-7">
          <b-form-input
            type="datetime-local"
            id="input-7"
            v-model="attendee.arrival_time"
            placeholder="Enter arrival time"
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Other detail:" label-for="input-8">
          <b-form-input
            id="input-8"
            v-model="attendee.other_detail"
            placeholder="Enter other detail"
          ></b-form-input>
        </b-form-group>

        <b-form-checkbox
          id="checkbox-1"
          name="checkbox-1"
          v-model="acceptedTerms"
          value="accepted"
          unchecked-value="not_accepted"
        >
          I've know what the conference is, and know what may happen after register.
        </b-form-checkbox>
      </b-modal>
      <b-modal id="modal-unregister" @ok="unregister" title="Unregister">
        <p class="my-4">Are you sure to unregister?</p>
      </b-modal>

      <p>{{status}}</p>
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

function input2date (str) {
  let date = new Date(str)
  return date
}

export default {
  computed: mapState({
    user: 'user'
  }),
  data () {
    return {
      pageSwitch: 0, // 0: first time loading, 1: normal, 2: admin
      isLoading: false,
      attendee: {
        name: '',
        acceptedTerms: false,
        transport_type: null,
        transport_id: '',
        depart_station: '',
        depart_time: date2input(new Date()),
        arrival_station: '',
        arrival_time: date2input(new Date()),
        other_detail: ''
      },
      transport_options: [
        { value: 'Flight', text: '航班' },
        { value: 'Train', text: '列车' },
        { value: 'Other', text: '其他' },
        { value: null, text: '未决定' }
      ],
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
      status: ''
    }
  },
  mounted () {
    this.isLoading = true
    this.axios.get('/api/event/' + this.$route.params.id)
      .then(res => {
        console.log('init')
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

    realRegister (id) {
      var info = {
        event_id: this.$route.params.id
      }
      if (id !== null) { info.transport_id = id }

      this.axios.post('/api/register/', info)
        .then(res => {
          this.event.registered = true
          this.isLoading = false
          if (res.status === 201) {
            this.status = 'Register successfully'
          } else {
            this.status = 'Fail to register: status != 201'
            alert(JSON.stringify(res.data))
          }
        })
        .catch(err => {
          this.isLoading = false
          this.status = 'Fail to register: other error'
          console.log(err)
        })
    },
    register (evt) {
      if (!this.acceptedTerms ||
         (this.attendee.transport_type !== null &&
         (this.attendee.transport_id === '' || this.attendee.arrival_time === ''))
      ) {
        if (!this.acceptedTerms) {
          alert('Pleast accept the terms first')
        } else {
          if (this.attendee.transport_id === '') {
            alert('Please give transport id')
          } else {
            if (this.attendee.arrival_time === '') {
              alert('Pleast give arrival time')
            }
          }
        }
        this.status = 'Fail to register'
        evt.preventDefault()
        return
      }
      this.status = 'Registering...'
      this.isLoading = true
      console.log('Trying to register')
      if (this.user === null) {
        this.isLoading = false
        this.status = 'Please login first'
      } else {
        console.log('id=' + this.$route.params.id)
        if (this.attendee.transport_type !== null) {
          this.axios.post('/api/trans/', {
            event_id: this.$route.params.id,
            transport_type: this.attendee.transport_type,
            transport_id: this.attendee.transport_id,
            depart_station: this.attendee.depart_station,
            depart_time: input2date(this.attendee.depart_time).toISOString(),
            arrival_station: this.attendee.arrival_station,
            arrival_time: input2date(this.attendee.arrival_time).toISOString(),
            other_detail: this.attendee.other_detail
          })
            .then(res => {
              console.log(res.data)
              if (res.status === 201) {
                this.realRegister(res.data.id)
              } else {
                this.isLoading = false
                this.status = 'Fail to provide transport: status != 201'
                alert(JSON.stringify(res.data))
              }
            })
            .catch(err => {
              this.isLoading = false
              this.status = 'Fail to provide transport: other error'
              console.log(err)
            })
        } else {
          this.realRegister(null)
        }
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
              this.status = null
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
