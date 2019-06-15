<template>
  <b-container>
    <h2>{{ $t('Registered Events') }}</h2>

    <TableLayout
      :item-name="$t('Event')"
      :refresh="refresh"
      :total-rows="userRegisterEvent.length"
    >
      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="userRegisterEvent"
          :fields="fields"
          primary-key="id"
        >
          <template #eventInfo.title="row">
            <b-link :to="'/event/' + row.item.eventInfo.id">
              {{ row.value }}
            </b-link>
          </template>

          <template #transportInfo="row">
            <div v-if="row.value">
              {{ row.value.departStation }} <br>
              {{ row.value.departTime.toLocaleString() }}
            </div>
            <div v-else>
              {{ $t('None') }}
            </div>
          </template>

          <template #approved="row">
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="minus"
              :style="{ color: '#2196F3' }"
            />
          </template>

          <template #checkedIn="row">
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="minus"
              :style="{ color: '#2196F3' }"
            />
          </template>

          <template #actions="row">
            <b-button
              size="sm"
              @click="row.toggleDetails"
            >
              {{ row.detailsShowing ? $t('Hide Details') : $t('Show Details') }}
            </b-button>
          </template>

          <template #row-details="row">
            <b-card-group deck>
              <b-card
                :header="$t('Event Information')"
              >
                <b-card-text>
                  <h6> {{ row.item.eventInfo.title }} </h6>
                  <strong>{{ $t('At') }}</strong> {{ row.item.eventInfo.location }} <br>
                  <strong>{{ $t('From') }}</strong> {{ row.item.eventInfo.startTime.toLocaleString() }} <br>
                  <strong>{{ $t('To') }}</strong> {{ row.item.eventInfo.endTime.toLocaleString() }} <br>
                </b-card-text>
              </b-card>
              <b-card>
                <template #header>
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mt-1">
                      {{ $t('Transport') }} &amp; {{ $t('Accommodation') }}
                    </h6>
                    <b-button
                      variant="success"
                      size="sm"
                      @click="editTransport(row)"
                    >
                      {{ $t('Edit') }}
                    </b-button>
                  </div>
                </template>
                <b-card-text v-if="row.item.transportInfo">
                  <strong>{{ row.item.transportInfo.transportType }}</strong> {{ row.item.transportInfo.transportId }} <br>
                  <strong>{{ $t('From') }}</strong> {{ row.item.transportInfo.departStation }} <br>
                  {{ row.item.transportInfo.departTime.toLocaleString() }} <br>
                  <strong>{{ $t('To') }}</strong> {{ row.item.transportInfo.arrivalStation }} <br>
                  {{ row.item.transportInfo.arrivalTime.toLocaleString() }}
                  <div v-if="row.item.transportInfo.accommodation">
                    <strong>{{ $t('Stay at') }} </strong> {{ row.item.transportInfo.accommodation }}
                  </div>
                  <div v-if="row.item.transportInfo.otherDetail">
                    <strong>{{ $t('p.s.') }}</strong> {{ row.item.transportInfo.otherDetail }}
                  </div>
                </b-card-text>
                <b-card-text v-else>
                  {{ $t('None') }}
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
import { BButton, BTable, BLink, BCardGroup, BCard, BCardText } from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'
import TransportModal from '@/components/TransportModal.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMinus, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faMinus, faCheck)

export default {
  name: 'UserRegisterEvent',
  components: {
    FontAwesomeIcon,
    TableLayout,
    TransportModal,
    BButton,
    BTable,
    BLink,
    BCardGroup,
    BCard,
    BCardText
  },
  data () {
    return {
      userRegisterEvent: []
    }
  },
  computed: {
    fields () {
      return [
        {
          key: 'eventInfo.title',
          label: this.$t('Event')
        },
        {
          key: 'eventInfo.startTime',
          label: this.$t('Start time'),
          sortable: true,
          formatter: value => value.toLocaleString()
        },
        {
          key: 'transportInfo',
          label: this.$t('Depart Info')
        },
        {
          key: 'approved',
          label: this.$t('Approve status')
        },
        {
          key: 'checkedIn',
          label: this.$t('Check-in status')
        },
        {
          key: 'actions',
          label: this.$t('Actions')
        }
      ]
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
      this.$refs['tp-modal'].resetShow(item.transportInfo, item.eventInfo.id)
        .then(transport => {
          if (transport !== false) {
            item.transportInfo = transport
          }
        })
    }
  }
}
</script>

<style scoped>
/* .card-detail {
  text-align: left;
} */
</style>
