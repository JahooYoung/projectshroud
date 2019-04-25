<template>
  <div>
    <b-container>
      <h2>Admin Events</h2>
      <b-row>
        <b-col
          md="4"
          class="my-1"
        >
          <b-input-group>
            <b-input-group-text slot="prepend">
              Filter
            </b-input-group-text>
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
        </b-col>

        <b-table
          striped
          hover
          show-empty
          :busy="isLoading"
          :items="events"
          :fields="fields"
          primary-key="event.id"
          :filter="filter"
          sort-by="start_time"
        >
          <div
            slot="table-busy"
            class="text-center text-danger my-2"
          >
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>

          <template
            slot="event_info.title"
            slot-scope="row"
          >
            <b-link :to="'/event/' + row.item.event_info.id">
              {{ row.value }}
            </b-link>
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
const fields = [
  { key: 'event_info.title', label: 'event' },
  { key: 'event_info.start_time', label: 'time', sortable: true },
  // { key: 'host_display_info', label: 'Host', sortable: true },
  { key: 'transport_info', label: 'transport' },
  { key: 'actions' }
]

export default {
  data () {
    return {
      filter: null,
      fields,
      events: []
    }
  },
  created () {
    this.axios.get('/api/event/admins/')
      .then(res => {
        this.events = res.data
      })
  }
}
</script>
