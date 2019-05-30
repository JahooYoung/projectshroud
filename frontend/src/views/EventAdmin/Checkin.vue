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
          primary-key="checkinToken"
        >
          <template #activate="row">
            <b-button
              v-if="!row.item.started"
              size="sm"
              variant="primary"
              @click="toggle(row.item)"
            >
              Activate
            </b-button>
            <b-button
              v-else
              size="sm"
              variant="warning"
              @click="toggle(row.item)"
            >
              Inactivate
            </b-button>
          </template>

          <template #QRcode="row">
            <b-button
              variant="outline-dark"
              size="sm"
              @click="showQRcode(row.item)"
            >
              Show QRcode
            </b-button>
          </template>

          <template #delete="row">
            <b-button
              variant="danger"
              size="sm"
              @click="deleteChannel(row.item)"
            >
              Delete
            </b-button>
          </template>
        </b-table>
      </template>
    </TableLayout>

    <b-modal
      ref="add-channel"
      title="Add new channel"
      ok-title="Add"
      @shown="$refs['channel-name-input'].focus()"
      @ok="addChannel()"
    >
      <b-form @submit.prevent="$refs['add-channel'].hide(), addChannel()">
        <b-form-group
          label="Channel name:"
          label-for="channel-name-input"
          label-cols-lg="3"
        >
          <b-form-input
            id="channel-name-input"
            ref="channel-name-input"
            v-model="newChannelName"
          />
        </b-form-group>
      </b-form>
    </b-modal>

    <b-modal
      ref="show-QRcode"
      :title="'QRcode For Channel ' + currentChannelName"
      size="lg"
    >
      <b-img
        v-if="qrcodeURL"
        center
        fluid
        :src="qrcodeURL"
        alt="Qrcode cannot display correctly"
      />
    </b-modal>
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'

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
          key: 'count',
          label: 'Attendee Count',
          sortable: true
        },
        {
          key: 'activate',
          label: 'Activate'
        },
        {
          key: 'QRcode',
          label: 'QRcode'
        },
        {
          key: 'delete',
          label: 'Delete'
        }
      ],
      channel: [],
      newChannelName: '',
      currentChannelName: '',
      qrcodeURL: null
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
    async refresh () {
      const res = await this.axios.get(`/api/event/${this.eventId}/checkin/`)
      this.channel = res.data
    },
    async addChannel () {
      try {
        await this.axios.post(`/api/event/${this.eventId}/checkin/`, {
          name: this.newChannelName
        })
        this.toastSuccess('Successfully added channel ' + this.newChannelName)
        this.newChannelName = ''
        this.refresh()
      } catch (err) {
        if (err.needHandle) {
          this.toastError('Failed to add channel ' + this.newChannelName)
        }
      }
    },
    async toggle (channel) {
      await this.axios.post(`/api/checkin/${channel.checkinToken}/toggle/`)
      this.refresh()
    },
    async deleteChannel (channel) {
      const message = 'Are you sure?'
      const answer = await this.$bvModal.msgBoxConfirm(message, {
        // centered: true,
        title: 'Confirm Deletion'
      })
      if (answer) {
        await this.axios.delete(`/api/checkin/${channel.checkinToken}/delete/`)
        this.refresh()
      }
    },
    async showQRcode (channel) {
      this.currentChannelName = channel.name
      try {
        await this.getQrcode(channel)
        this.$refs['show-QRcode'].show()
      } catch (err) {
        if (err.needHandle) {
          this.toastError('Failed to get QRcode')
        }
      }
    },
    async getQrcode (channel) {
      const url = `${window.location.origin}/checkin/?token=${channel.checkinToken}&id=${this.eventId}`
      console.log(url)
      const res = await this.axios.post('/api/qrcode/', {
        text: url
      }, {
        responseType: 'blob'
      })
      const qrcode = new Blob([res.data], { type: 'image/png' })
      this.qrcodeURL = URL.createObjectURL(qrcode)
    }
  }
}
</script>
