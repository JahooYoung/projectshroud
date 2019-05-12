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
          <div
            slot="table-busy"
            class="text-center text-primary my-2"
          >
            <b-spinner class="align-middle mr-2" />
            <strong>Loading...</strong>
          </div>

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
              :style="{ color: 'blue' }"
              class="ml-3"
              @click="assignAdmin(row.item)"
            />
          </template>
        </b-table>
      </template>
    </TableLayout>
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
        {
          key: 'date_registered',
          label: 'Registered Time',
          formatter: t => t.toLocaleString()
        },
        {
          key: 'transport_info',
          label: 'Arrive Time'
        },
        {
          key: 'checked_in',
          label: 'Checked in'
        },
        {
          key: 'is_admin',
          label: 'Is Admin'
        }
      ],
      attendee: []
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
    refresh () {
      this.axios.get(`/api/event/${this.eventId}/attendee/`)
        .then(res => {
          this.attendee = res.data
        })
    },
    manualCheckIn (rowItem) {
      // Todo
    },
    assignAdmin (rowItem) {
      this.axios.post('/api/assignadmin/', {
        user_id: rowItem.user_info.id,
        event_id: this.eventId
      })
        .then(() => {
          rowItem.is_admin = true
        })
    }
  }
}
</script>
