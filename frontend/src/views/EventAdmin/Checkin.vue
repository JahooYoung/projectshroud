<template>
  <b-container>
    <h2> Channel List</h2>

    <TableLayout
      item-name="channel"
      :refresh="refresh"
      :total-rows="channel.length"
    >
      <template #buttons>
        <b-button
          class="mr-2"
          variant="outline-dark"
          @click="$refs['add-channel'].show()"
        >
          Add channel
        </b-button>
      </template>

      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="channel"
          :fields="fields"
          primary-key="token"
        >
          <template #activate="row">
            <b-button
              v-if="row.item.started"
              size="sm"
              variant="primary"
              @click="toggle(row.item)"
            >
              Activate
            </b-button>
            <b-button
              v-else
              size="sm"
              variant="danger"
              @click="toggle(row.item)"
            >
              Inactivate
            </b-button>
          </template>

          <template #QRcode="row">
            <b-button
              size="sm"
              variant="primary"
              @click="showQRcode(row.item)"
            >
              Show QRcode
            </b-button>
          </template>
        </b-table>
      </template>
    </TableLayout>

    <b-modal
      ref="add-channel"
      ok-title="Add"
      @ok="addChannel()"
    >
      <b-form-group
        label="Channel name:"
        label-for="channel-name"
        label-cols-lg="3"
      >
        <b-form-input
          id="channel-name"
          v-model="newChannelName"
        />
      </b-form-group>
    </b-modal>

    <b-modal
      ref="show-QRcode"
      lazy
      size="lg"
    >
      <b-img
        v-if="checkingIn && qrcodeURL"
        center
        fluid
        :src="qrcodeURL"
        alt="Qrcode cannot display correctly"
      />
    </b-modal>
    <!-- <b-button
      size="lg"
      :variant="checkingIn ? 'danger' : 'primary'"
      :disabled="isLoading"
      @click="onClick"
    >
      <b-spinner
        v-show="isLoading"
        small
        type="grow"
      />
      {{ checkingIn ? 'Stop' : 'Start' }} Check In
    </b-button>
    -->
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'

// Send event_id
// Return name,token,started,(count),

export default {
  name: 'EventAdminCheckin',
  components: {
    TableLayout
  },
  data () {
    return {
      fields: [
        {
          key: 'name',
          label: 'Location',
          sortable: true
        },
        {
          key: 'activate',
          label: 'activate'
        },
        {
          key: 'QRcode',
          label: 'QRcode'
        }
      ],
      channel: [],
      checkingIn: false,
      checkinToken: null,
      qrcodeURL: null,
      location: window.location
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
    onClick () {
      if (this.checkingIn) {
        this.qrcodeURL = null
        this.axios.delete(`/api/checkin/${this.checkinToken}/stop/`)
          .then(res => {
            this.checkingIn = false
          })
      } else {
        this.axios.post('/api/checkin/start/', {
          eventId: this.eventId
        })
          .then(res => {
            this.checkingIn = true
            this.checkinToken = res.data.checkinToken
            this.getQrcode()
          })
      }
    },
    refresh () {
      this.axios.get(`/api/event/${this.eventId}/checkin/`)
        .then(res => {
          this.channels = res.data
          // this.checkingIn = true
          // this.checkinToken = res.data.checkinToken
          // this.getQrcode()
        })
    },
    addChannel () {
      this.axios.post(`/api/event/${this.eventId}/checkin/`, {
        name: this.newChannelName
      })
        .then(res => {
          this.refresh()
        })
        .catch(() => {
        })
    },
    toggle (channel) {
      this.axios.post(`/api/checkin/${channel.token}/toggle/`, {

      })
        .then(res => {
          this.refresh()
        })
    },
    showQRcode (channel) {

    },
    getQrcode (channel) {
      const url = `${this.location.origin}/checkin/?token=${channel.token}&id=${this.eventId}`
      console.log(url)
      this.axios.post('/api/qrcode/', {
        text: url
      }, {
        responseType: 'blob'
      })
        .then(res => {
          const qrcode = new Blob([res.data], { type: 'image/png' })
          this.qrcodeURL = URL.createObjectURL(qrcode)
        })
    }
  }
}
</script>
