<template>
  <b-container>
    <h2>Registered Events</h2>

    <TableLayout
      item-name="event"
      :refresh="refresh"
      :total-rows="userRegisterEvent.length"
    >
      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="userRegisterEvent"
          :fields="fields"
          :tbody-tr-class="rowClass"
          primary-key="id"
        >
          <template #event_info.title="row">
            <b-link :to="'/event/' + row.item.event_info.id">
              {{ row.value }}
            </b-link>
          </template>

          <template #transport_info="row">
            <div v-if="row.value">
              {{ row.value.depart_station }} <br>
              {{ row.value.depart_time.toLocaleString() }}
            </div>
            <div v-else>
              None
            </div>
          </template>

          <template #checked_in="row">
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="minus"
              :style="{ color: '#2196F3' }"
            />
          </template>

          <template #actions="row">
            <b-button
              size="sm"
              @click="row.toggleDetails"
            >
              {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
            </b-button>
          </template>

          <template #row-details="row">
            <b-card-group deck>
              <b-card
                header="Event Information"
              >
                <b-card-text>
                  <h6> {{ row.item.event_info.title }} </h6>
                  <strong>At</strong> {{ row.item.event_info.location }} <br>
                  <strong>From</strong> {{ row.item.event_info.start_time.toLocaleString() }} <br>
                  <strong>To</strong> {{ row.item.event_info.end_time.toLocaleString() }} <br>
                </b-card-text>
              </b-card>
              <b-card>
                <template #header>
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mt-1">
                      Your Transport
                    </h6>
                    <b-button
                      variant="success"
                      size="sm"
                      @click="editTransport(row)"
                    >
                      Edit
                    </b-button>
                  </div>
                </template>
                <b-card-text v-if="row.item.transport_info">
                  <strong>{{ row.item.transport_info.transport_type }}</strong> {{ row.item.transport_info.transport_id }} <br>
                  <strong>From</strong> {{ row.item.transport_info.depart_station }} <br>
                  {{ row.item.transport_info.depart_time.toLocaleString() }} <br>
                  <strong>To</strong> {{ row.item.transport_info.arrival_station }} <br>
                  {{ row.item.transport_info.arrival_time.toLocaleString() }}
                </b-card-text>
                <b-card-text v-else>
                  None
                </b-card-text>
              </b-card>
            </b-card-group>
          </template>
        </b-table>
      </template>
    </TableLayout>
    <transport-modal ref="tp-modal" />
  </b-container>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMinus, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import TableLayout from '@/components/TableLayout.vue'
import TransportModal from '@/components/TransportModal.vue'

library.add(faMinus, faCheck)

export default {
  name: 'UserRegisterEvent',
  components: {
    FontAwesomeIcon,
    TableLayout,
    TransportModal
  },
  data () {
    return {
      fields: [
        {
          key: 'event_info.title',
          label: 'Event'
        },
        {
          key: 'event_info.start_time',
          label: 'Start Time',
          sortable: true,
          formatter: value => value.toLocaleString()
        },
        {
          key: 'transport_info',
          label: 'Depart Info'
        },
        {
          key: 'checked_in',
          label: 'Checked in'
        },
        {
          key: 'actions'
        }
      ],
      userRegisterEvent: []
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    async refresh () {
      try {
        const res = await this.axios.get('/api/event/registered/')
        this.userRegisterEvent = res.data
      } catch (err) {
        // do nothing?
      }
    },
    editTransport (row) {
      const item = this.userRegisterEvent[row.index]
      this.$refs['tp-modal'].resetShow(item.transport_info, item.event_info.id)
        .then(transport => {
          if (transport !== false) {
            item.transport_info = transport
          }
        })
    }
  }
}
</script>

<style scoped>
.card-detail {
  text-align: left;
}
</style>
