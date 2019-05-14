<template>
  <div>
    <b-spinner
      v-if="refreshing"
      style="width: 3rem; height: 3rem;"
      label="Loading..."
    />
    <b-container v-else>
      <b-row>
        <b-col
          cols="12"
          order="2"
          lg="9"
          order-lg="1"
        >
          <b-card header="Event Description">
            <div
              v-if="event"
              class="markdown-body"
              style="text-align: initial;"
              v-html="event.descriptionHtml"
            />
            <b-card-title v-else>
              This event does not exist
            </b-card-title>
          </b-card>
        </b-col>
        <b-col
          v-if="event"
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
                  <div
                    v-if="event.requireApprove"
                    class="mb-2"
                  >
                    <b v-if="!event.eventRegistered">
                      <font-awesome-icon
                        icon="file-alt"
                      />
                      Require approvement
                    </b>
                    <b v-else-if="!event.userRegisterEvent.approved">
                      <font-awesome-icon
                        icon="circle-notch"
                        class="fa-spin"
                        :style="{ color: '#2196F3' }"
                      />
                      Waiting for approvement
                    </b>
                    <b v-else>
                      <font-awesome-icon
                        icon="check"
                        :style="{ color: 'green' }"
                      />
                      Approved
                    </b>
                  </div>
                  <b-button
                    v-if="!event.eventRegistered"
                    variant="primary"
                    :disabled="isLoading"
                    @click="checkActivated() && $refs['modal-register'].show()"
                  >
                    Register
                  </b-button>
                  <b-button
                    v-else
                    variant="danger"
                    :disabled="isLoading"
                    @click="$refs['modal-unregister'].show()"
                  >
                    Unregister
                  </b-button>
                </b-list-group-item>
                <b-list-group-item v-if="event.eventAdmin">
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
              v-if="event.eventRegistered"
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
                <strong>{{ transport.transportType }}</strong> {{ transport.transportId }} <br>
                <strong>From</strong> {{ transport.departStation }} <br>
                {{ transport.departTime.toLocaleString() }} <br>
                <strong>To</strong> {{ transport.arrivalStation }} <br>
                {{ transport.arrivalTime.toLocaleString() }}
                <div v-if="transport.otherDetail">
                  <strong>p.s.</strong> {{ transport.otherDetail }}
                </div>
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
      <div
        class="my-2"
        align="center"
      >
        Are you sure to register? <br>
        You can also provide your transport info
        <div v-if="event.requireApprove">
          <hr>
          <b>Application Text</b>
          <b-textarea
            v-model="applicationText"
            class="application-text"
            rows="5"
          />
        </div>
        <div v-if="conflictEvent">
          <hr>
          <b>Warning</b>: this event is in conflict with <br>
          <b-link
            :to="`/event/${conflictEvent.id}`"
            @click="$refs['modal-register'].hide()"
          >
            {{ conflictEvent.title }}
          </b-link> <br>
          It starts at {{ conflictEvent.startTime.toLocaleString() }} <br>
          and ends at {{ conflictEvent.endTime.toLocaleString() }}
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
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCircleNotch, faCheck, faFileAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faCircleNotch, faCheck, faFileAlt)

export default {
  name: 'EventDetail',
  components: {
    TransportModal,
    FontAwesomeIcon
  },
  data () {
    return {
      event: null,
      applicationText: '',
      transport: null,
      conflictEvent: null,
      refreshing: false
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
      this.$root.$bvToast.toast(message, {
        title: succeed ? 'Succeed' : 'Error',
        variant: succeed ? 'default' : 'danger',
        autoHideDelay: 3000,
        solid: true
      })
    },
    async refresh () {
      this.refreshing = true
      try {
        const res = await this.axios.get(`/api/event/${this.eventId}/`)
        this.event = res.data
        if (this.event.userRegisterEvent) {
          this.transport = this.event.userRegisterEvent.transportInfo
        } else {
          this.transport = null
          this.$nextTick(() => {
            this.$refs['tp-modal'].reset()
          })
        }
      } catch (err) {
        this.event = null
      }
      this.refreshing = false
    },
    async checkConflict () {
      try {
        const res = await this.axios.post('/api/reg-conflict/', {
          eventId: this.eventId
        })
        if (res.data.conflict) {
          this.conflictEvent = res.data.userRegisterEvent.eventInfo
        } else {
          this.conflictEvent = null
        }
      } catch (err) {
        // do nothing
      }
    },
    async register () {
      try {
        const res = await this.axios.post('/api/register/', {
          eventId: this.eventId,
          applicationText: this.applicationText || undefined
        })
        this.event.eventRegistered = true
        this.event.userRegisterEvent = res.data
        this.makeToast(true, 'Register successfully')
      } catch (err) {
        if (err.response && err.response.status === 400) {
          this.makeToast(false, err.response.data.detail)
        }
      }
    },
    async registerAndTransport () {
      await this.register()
      if (this.event.eventRegistered) {
        await this.editTransport()
      }
    },
    async unregister () {
      try {
        await this.axios.post('/api/unregister/', {
          eventId: this.eventId
        })
        this.event.eventRegistered = false
        this.event.userRegisterEvent = null
        this.makeToast(true, 'Unegister successfully')
      } catch (err) {
        if (err.response) {
          this.makeToast(false, err.response.data.detail)
        }
      }
    },
    async editTransport () {
      const transport = await this.$refs['tp-modal'].show(
        this.transport,
        this.eventId
      )
      if (transport !== false) {
        this.transport = transport
      }
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

/* .application-text {
  border: 1px solid;
} */

.fa-spin {
  -webkit-animation: fa-spin 2s infinite linear;
  animation: fa-spin 2s infinite linear;
}
</style>
