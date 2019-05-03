<template>
  <b-container>
    <h2>Attendee List</h2>

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
        </b-table>
      </template>
    </TableLayout>
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimes, faCheck)
// Vue.component('font-awesome-icon', FontAwesomeIcon)

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
          formatter: t => new Date(t).toLocaleString()
        },
        {
          key: 'transport_info',
          label: 'Arrive Time'
        },
        {
          key: 'checked_in',
          label: 'Checked in'
        }
      ],
      attendee: []
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/' + this.$route.params.id + '/attendee/')
        .then(res => {
          this.attendee = res.data
        })
    },
    manualCheckIn (rowItem) {
      // Todo
    }
  }
}
</script>
