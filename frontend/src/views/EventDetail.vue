<template>
  <div>
    <b-spinner
      v-if="firstLoading"
      style="width: 3rem; height: 3rem;"
      label="Loading..."
    />

    <div v-else>
      <b-container>
        <b-row>
          <b-col cols="9">
            <b-card header="Event Description">
              <div
                v-if="event.title"
                class="markdown-body"
                style="text-align: initial;"
                v-html="event.description_html"
              />
              <b-card-title v-else>
                Event is not existed
              </b-card-title>
            </b-card>
          </b-col>
          <b-col
            v-if="event.title !== ''"
            cols="3"
          >
            <b-card
              header="Event Information"
              class="right-card"
            >
              <b-card-body>
                <h6> {{ event.title }} </h6>
                <strong>At</strong> {{ event.location }} <br>
                <strong>From</strong> {{ new Date(event.startTime).toLocaleString() }} <br>
                <strong>To</strong> {{ new Date(event.endTime).toLocaleString() }} <br>
              </b-card-body>

              <b-list-group flush>
                <b-list-group-item>
                  <b-button
                    v-if="!event.registered"
                    variant="primary"
                    :disabled="isLoading"
                    @click="checkActivated() && $bvModal.show('modal-register')"
                  >
                    <b-spinner
                      v-show="isLoading"
                      small
                      type="grow"
                    />
                    Register
                  </b-button>
                  <b-button
                    v-else
                    variant="danger"
                    :disabled="isLoading"
                    @click="checkActivated() && $bvModal.show('modal-unregister')"
                  >
                    <b-spinner
                      v-show="isLoading"
                      small
                      type="grow"
                    />
                    Unregister
                  </b-button>
                </b-list-group-item>
                <b-list-group-item v-if="isAdmin">
                  <b-button
                    variant="dark"
                    :to="`/event/${$route.params.id}/admin`"
                  >
                    Manage this event
                  </b-button>
                </b-list-group-item>
              </b-list-group>
            </b-card>
          </b-col>
        </b-row>
      </b-container>

      <b-modal
        id="modal-register"
        title="Basic infomation"
        @ok="register"
      >
        <b-form-group
          label="Your Name:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="attendee.name"
            placeholder="Enter name"
          />
        </b-form-group>

        <b-form-group
          label="Your transport type:"
          label-for="input-2"
        >
          <b-form-select
            id="input-2"
            v-model="attendee.transport_type"
            :options="transport_options"
          />
        </b-form-group>

        <b-form-group
          label="Your transport id:"
          label-for="input-3"
        >
          <b-form-input
            id="input-3"
            v-model="attendee.transport_id"
            placeholder="Enter transport id"
          />
        </b-form-group>

        <b-form-group
          label="Your depart station:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="attendee.depart_station"
            placeholder="Enter depart station"
          />
        </b-form-group>

        <b-form-group
          label="Your depart_time:"
          label-for="input-5"
        >
          <b-form-input
            id="input-5"
            v-model="attendee.depart_time"
            type="datetime-local"
            placeholder="Enter depart time"
          />
        </b-form-group>

        <b-form-group
          label="Your arrival_station:"
          label-for="input-6"
        >
          <b-form-input
            id="input-6"
            v-model="attendee.arrival_station"
            placeholder="Enter arrival station"
          />
        </b-form-group>

        <b-form-group
          label="Your arrival time:"
          label-for="input-7"
        >
          <b-form-input
            id="input-7"
            v-model="attendee.arrival_time"
            type="datetime-local"
            placeholder="Enter arrival time"
          />
        </b-form-group>

        <b-form-group
          label="Other detail:"
          label-for="input-8"
        >
          <b-form-input
            id="input-8"
            v-model="attendee.other_detail"
            placeholder="Enter other detail"
          />
        </b-form-group>
      </b-modal>
      <b-modal
        id="modal-unregister"
        title="Unregister"
        @ok="unregister"
      >
        <p class="my-4">
          Are you sure to unregister?
        </p>
      </b-modal>
    </div>
  </div>
</template>

<script>
import 'mavon-editor/dist/markdown/github-markdown.min.css'

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
  name: 'EventDetail',
  data () {
    return {
      firstLoading: true,
      isAdmin: false,
      attendee: {
        name: '',
        transport_type: null,
        transport_id: '',
        depart_station: '',
        depart_time: date2input(new Date()),
        arrival_station: '',
        arrival_time: date2input(new Date()),
        other_detail: ''
      },
      acceptedTerms: true,
      transport_options: [
        { value: 'Flight', text: '航班' },
        { value: 'Train', text: '列车' },
        { value: 'Other', text: '其他' },
        { value: null, text: '未决定' }
      ],
      event: {
        title: null,
        description: '',
        description_html: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        registered: false,
        requireApprove: false
      }
    }
  },
  watch: {
    '$route': 'refresh'
  },
  created () {
    this.refresh()
      .then(() => {
        this.firstLoading = false
      })
  },
  methods: {
    makeToast (succeed, message) {
      this.$bvToast.toast(message, {
        title: succeed ? 'Succeed' : 'Error',
        variant: succeed ? 'default' : 'danger',
        autoHideDelay: 3000,
        solid: true
      })
    },
    refresh () {
      return this.axios.get('/api/event/' + this.$route.params.id)
        .then(res => {
          this.event.title = res.data.title
          this.event.description = res.data.description
          this.event.description_html = res.data.description_html
          this.event.startTime = date2input(new Date(res.data.start_time))
          this.event.endTime = date2input(new Date(res.data.end_time))
          this.event.location = res.data.location
          this.event.public = res.data.public
          this.event.registered = res.data.event_registered
          this.event.requireApprove = res.data.require_approve
          this.isAdmin = res.data.event_admin
        })
        .catch(err => {
          this.event.title = ''
          if (err.response) {
            this.makeToast(false, err.response)
          }
        })
    },
    postRegister (transportId) {
      const info = {
        event_id: this.$route.params.id
      }
      if (transportId !== null) {
        info.transport_id = transportId
      }
      return this.axios.post('/api/register/', info)
        .then(res => {
          this.event.registered = true
          this.makeToast(true, 'Register successfully')
        })
        .catch(err => {
          if (err.response) {
            this.makeToast(false, err.response.data.detail)
          }
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

      if (this.attendee.transport_type === null) {
        this.postRegister(null)
        return
      }
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
          return this.postRegister(res.data.id)
        })
        .catch(err => {
          if (err.response) {
            this.makeToast(false, err.response.data.detail)
          }
        })
    },
    unregister () {
      this.axios.post('/api/unregister/', {
        event_id: this.$route.params.id
      })
        .then(res => {
          this.event.registered = false
          this.makeToast(true, 'Unegister successfully')
        })
        .catch(err => {
          if (err.response) {
            this.makeToast(false, err.response.data.detail)
          }
        })
    }
  }
}
</script>

<style scoped>
.right-card {
  position: fixed;
  margin-right: 3em;
}
</style>
