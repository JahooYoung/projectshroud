<template>
  <div>
    <b-container>
      <b-row>
        <b-col
          cols="12"
          order="2"
          lg="9"
          order-lg="1"
        >
          <b-card header="Event Description">
            <div
              v-if="event.title"
              class="markdown-body"
              style="text-align: initial;"
              v-html="event.descriptionHtml"
            />
            <b-card-title v-else>
              Event is not existed
            </b-card-title>
          </b-card>
        </b-col>
        <b-col
          v-if="event.title !== ''"
          cols="12"
          order="1"
          lg="3"
          order-lg="2"
        >
          <div class="right-card">
            <b-card
              header="Event Information"
              class="mb-2"
            >
              <b-card-text>
                <h6> {{ event.title }} </h6>
                <strong>At</strong> {{ event.location }} <br>
                <strong>From</strong> {{ event.startTime.toLocaleString() }} <br>
                <strong>To</strong> {{ event.endTime.toLocaleString() }} <br>
              </b-card-text>

              <b-list-group flush>
                <b-list-group-item>
                  <b-button
                    v-if="!event.registered"
                    variant="primary"
                    :disabled="isLoading"
                    @click="checkActivated() && $refs['modal-register'].show()"
                  >
                    <!-- <b-spinner
                      v-show="isLoading"
                      small
                      type="grow"
                    /> -->
                    Register
                  </b-button>
                  <b-button
                    v-else
                    variant="danger"
                    :disabled="isLoading"
                    @click="$refs['modal-unregister'].show()"
                  >
                    <!-- <b-spinner
                      v-show="isLoading"
                      small
                      type="grow"
                    /> -->
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
            <b-card
              v-if="event.registered"
              class="mb-2"
            >
              <template #header>
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mt-1">
                    Your Transport
                  </h6>
                  <b-button
                    variant="success"
                    size="sm"
                    @click="editTransport"
                  >
                    Edit
                  </b-button>
                </div>
              </template>
              <b-card-text v-if="transport">
                <strong>{{ transport.transport_type }}</strong> {{ transport.transport_id }} <br>
                <strong>From</strong> {{ transport.depart_station }} <br>
                {{ new Date(transport.depart_time).toLocaleString() }} <br>
                <strong>To</strong> {{ transport.arrival_station }} <br>
                {{ new Date(transport.arrival_time).toLocaleString() }}
              </b-card-text>
              <b-card-text v-else>
                None
              </b-card-text>
            </b-card>
          </div>
        </b-col>
      </b-row>
    </b-container>

    <b-modal
      ref="modal-register"
      title="Confirm Registration"
      @show="checkConflict"
      @ok="register"
    >
      <div class="my-3">
        Are you sure to register? <br>
        You can also provide your transport info
        <div v-if="conflictEvent">
          <hr>
          <b>Warning</b>: this event is in conflict with <br>
          <b-link
            :to="`/event/${conflictEvent.id}`"
            @click="$refs['modal-register'].hide()"
          >
            {{ conflictEvent.title }}
          </b-link> <br>
          It starts at {{ new Date(conflictEvent.start_time).toLocaleString() }} <br>
          and ends at {{ new Date(conflictEvent.end_time).toLocaleString() }}
        </div>
      </div>

      <template #modal-footer>
        <div class="ml-auto">
          <b-button
            variant="secondary"
            @click="$refs['modal-register'].hide()"
          >
            Cancel
          </b-button>
          <b-button
            variant="primary"
            class="ml-2"
            :disabled="isLoading"
            @click="$refs['modal-register'].hide(), register()"
          >
            Yes
          </b-button>
          <b-button
            variant="primary"
            class="ml-2"
            :disabled="isLoading"
            @click="$refs['modal-register'].hide(), registerAndTransport()"
          >
            Yes and Provide Transport
          </b-button>
        </div>
      </template>
    </b-modal>

    <b-modal
      ref="modal-unregister"
      title="Confirm Unregistration"
      @ok="unregister"
    >
      <p class="my-3">
        Are you sure to unregister? (Your transport info will be lost)
      </p>
    </b-modal>

    <transport-modal ref="tp-modal" />
  </div>
</template>

<script>
import 'mavon-editor/dist/markdown/github-markdown.min.css'
import TransportModal from '@/components/TransportModal.vue'

export default {
  name: 'EventDetail',
  components: {
    TransportModal
  },
  data () {
    return {
      isAdmin: false,
      event: {
        title: null,
        description: '',
        description_html: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        registered: false,
        userRegisterEvent: null,
        requireApprove: false
      },
      transport: null,
      conflictEvent: null
    }
  },
  computed: {
    eventId () {
      return this.$route.params.id
    }
  },
  watch: {
    '$route': 'refresh'
  },
  created () {
    this.refresh()
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
      return this.axios.get(`/api/event/${this.eventId}/`)
        .then(res => {
          this.event.title = res.data.title
          this.event.description = res.data.description
          this.event.descriptionHtml = res.data.description_html
          this.event.startTime = new Date(res.data.start_time)
          this.event.endTime = new Date(res.data.end_time)
          this.event.location = res.data.location
          this.event.public = res.data.public
          this.event.registered = res.data.event_registered
          this.event.userRegisterEvent = res.data.user_register_event
          if (this.event.userRegisterEvent) {
            this.transport = this.event.userRegisterEvent.transport_info
          } else {
            this.transport = null
            this.$nextTick(() => {
              this.$refs['tp-modal'].reset()
            })
          }
          this.event.requireApprove = res.data.require_approve
          this.isAdmin = res.data.event_admin
        })
        .catch(() => {
          this.event.title = ''
        })
    },
    async checkConflict () {
      try {
        const res = await this.axios.post('/api/reg-conflict/', {
          event_id: this.eventId
        })
        console.log(res)
        if (res.data.conflict) {
          this.conflictEvent = res.data.user_register_event.event_info
        } else {
          this.conflictEvent = null
        }
      } catch (err) {
        // do nothing
      }
    },
    register () {
      return this.axios.post('/api/register/', {
        event_id: this.eventId
      })
        .then(res => {
          this.event.registered = true
          this.makeToast(true, 'Register successfully')
        })
        .catch(err => {
          if (err.response && err.response.status === 400) {
            this.makeToast(false, err.response.data.detail)
          }
        })
    },
    registerAndTransport () {
      this.register()
        .then(() => {
          if (this.event.registered) {
            this.editTransport()
          }
        })
    },
    unregister () {
      this.axios.post('/api/unregister/', {
        event_id: this.eventId
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
    },
    editTransport () {
      this.$refs['tp-modal'].show(this.transport, this.eventId)
        .then(transport => {
          if (transport !== false) {
            this.transport = transport
          }
        })
    }
  }
}
</script>

<style scoped>
@media (min-width: 992px) {
  .right-card {
    position: fixed;
    margin-right: 2em;
    min-width: 22%;
  }
}
</style>
