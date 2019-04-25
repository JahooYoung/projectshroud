<template>
  <div>
    <h2>Attendee List</h2>
    <b-container>
      <b-row>
        <b-input-group class="w-25 my-3">
          <b-form-input
            v-model="filter"
            placeholder="Type to Search"
          />
          <b-input-group-append>
            <b-button
              :disabled="!filter"
              @click="filter = ''"
            >
              Clear
            </b-button>
          </b-input-group-append>
        </b-input-group>
        <div class="ml-auto my-3">
          <b-button
            class="mr-2"
            variant="outline-info"
            href="#"
          >
            Export
          </b-button>
          <b-button
            class="mr-2"
            variant="outline-info"
            href="#"
          >
            Add attendee
          </b-button>
          <b-button
            variant="outline-info"
            @click="refresh"
            :disabled="isLoading"
          >
            Refresh
          </b-button>
        </div>
      </b-row>
      <b-row>
        <b-table
          striped
          hover
          show-empty
          :fields="fields"
          primary-key="user_info.id"
          :items="attendee"
          :busy="isLoading"
          :filter="filter"
        >
          <div
            slot="table-busy"
            class="text-center text-danger my-2"
          >
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>

          <template
            slot="checked_in"
            slot-scope="row"
          >
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="check-circle"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.user_info.id"
              icon="times-circle"
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
                @click="manualCheckIn(row.item)"
                :disabled="row.value || true"
              >
                Manually check in
              </b-button>
            </b-popover>
          </template>

          <template
            slot="actions"
            slot-scope="row"
          >
            <b-button
              size="sm"
              @click="row.toggleDetails"
            >
              {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
            </b-button>
          </template>

          <template
            slot="row-details"
            slot-scope="row"
          >
            <b-card>
              <ul>
                <li
                  v-for="(value, key) in row.item"
                  :key="key"
                >
                  {{ key }}: {{ value }}
                </li>
              </ul>
            </b-card>
          </template>
        </b-table>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimesCircle, faCheckCircle } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimesCircle, faCheckCircle)
// Vue.component('font-awesome-icon', FontAwesomeIcon)

export default {
  name: 'EventAdminAttendee',
  components: {
    FontAwesomeIcon
  },
  data () {
    return {
      fields: [
        { key: 'user_info.real_name', label: 'Name' },
        { key: 'user_info.mobile', label: 'Mobile' },
        { key: 'date_registered', label: 'Registered Time' },
        { key: 'transport_info', label: 'Arrive Time' },
        { key: 'checked_in', label: 'Checked in' }
      ],
      filter: null,
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
