<template>
  <b-container>
    <h2>Attendee List</h2>

    <b-progress
      :value="30"
      class="my-2"
    />

    <TableLayout
      item-name="attendee"
      :refresh="refresh"
      :total-rows="attendee.length"
    >
      <template #buttons>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          Export
        </b-button>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          Add attendee
        </b-button>
      </template>

      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="attendee"
          :fields="fields"
          primary-key="user_info.id"
        >
          <template #transport_info="row">
            <div v-if="row.value">
              {{ row.value.depart_station }} <br>
              {{ row.value.depart_time.toLocaleString() }}
            </div>
            <div v-else>
              None
            </div>
          </template>

          <template #approve="row">
            <font-awesome-icon
              v-if="row.item.approved"
              icon="check"
              :style="{ color: 'green' }"
            />
            <b-button
              v-else
              size="sm"
              variant="warning"
              @click="approve(row.item)"
            >
              See detail
            </b-button>
          </template>

          <template
            slot="checked_in"
            slot-scope="row"
          >
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="times"
              :style="{ color: 'red' }"
            />
            <b-popover
              :target="'checkin-popover-' + row.item.user_info.id"
              triggers="hover focus"
            >
              <template slot="title">
                Manually check in (click to keep) (not impl.)
              </template>
              <b-button
                variant="success"
                :disabled="row.value || true"
                @click="manualCheckIn(row.item)"
              >
                Manually check in
              </b-button>
            </b-popover>
          </template>

          <template
            slot="is_admin"
            slot-scope="row"
          >
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="times"
              :style="{ color: 'red' }"
            />
            <font-awesome-icon
              v-if="!row.value"
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="plus"
              :style="{ color: '#2196F3' }"
              class="ml-3"
              @click="assignAdmin(row.item)"
            />
          </template>
        </b-table>
      </template>
    </TableLayout>

    <b-modal
      ref="modal-approve"
      ok-title="Accept"
      cancel-title="Reject"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <template #modal-title>
        {{ modalData && modalData.userInfo.realName }}'s application
      </template>
      <h5>Application Text:</h5>
      {{ modalData && (modalData.applicationText || 'Empty') }}
    </b-modal>
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimes, faCheck, faPlus)

export default {
  name: 'EventAdminAttendee',
  components: {
    TableLayout,
    FontAwesomeIcon
  },
  data () {
    return {
      fields: [
        {
          key: 'user_info.real_name',
          label: 'Name'
        },
        {
          key: 'user_info.mobile',
          label: 'Mobile'
        },
        // {
        //   key: 'date_registered',
        //   label: 'Registered Time',
        //   formatter: t => t.toLocaleString()
        // },
        {
          key: 'transport_info',
          label: 'Arrival Info',
          sortable: true
        },
        {
          key: 'approve',
          label: 'Approve',
          sortable: true
        },
        {
          key: 'checked_in',
          label: 'Checked in',
          sortable: true
        },
        {
          key: 'is_admin',
          label: 'Is Admin',
          sortable: true
        }
      ],
      attendee: [],
      modalCallback: null,
      modalData: null
    }
  },
  computed: {
    eventId () {
      return this.$route.params.id
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    async refresh () {
      const res = await this.axios.get(`/api/event/${this.eventId}/attendee/`)
      this.attendee = res.data
    },
    manualCheckIn (rowItem) {
      // Todo
    },
    async assignAdmin (rowItem) {
      try {
        await this.axios.post('/api/assignadmin/', {
          user_id: rowItem.user_info.id,
          event_id: this.eventId
        })
        rowItem.is_admin = true
      } catch (err) {
        this.toastError('Failed to assign admin')
      }
    },
    showApproveModal () {
      return new Promise(resolve => {
        this.modalCallback = answer => {
          this.modalCallback = null
          resolve(answer)
        }
        this.$refs['modal-approve'].show()
      })
    },
    async approve (rowItem) {
      this.modalData = rowItem
      const answer = await this.showApproveModal()
      if (answer !== null) {
        const user = rowItem.userInfo.realName
        try {
          await this.axios.post(`/api/approve/`, {
            userId: rowItem.userInfo.id,
            eventId: this.eventId,
            approve: answer
          })
          if (answer) {
            rowItem.approved = true
            this.toastSuccess('Succeed to approve user ' + user)
          } else {
            this.toastSuccess('Succeed to reject user ' + user)
          }
        } catch (err) {
          this.toastError('Failed to approve user ' + user)
        }
      }
    }
  }
}
</script>
