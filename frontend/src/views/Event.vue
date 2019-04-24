<template>
  <div>
    <b-container>
      <h2>Event List</h2>
      <b-row>
        <b-input-group class="w-25 my-3">
          <!-- <b-input-group-text slot="prepend">
            Filter
          </b-input-group-text> -->
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
          <!-- <b-button
            class="mr-2"
            variant="outline-info"
            to="/event/new"
          >
            New Event
          </b-button> -->
          <b-button
            variant="outline-info"
            to="/event/new"
          >
            New Event
          </b-button>
        </div>

        <!-- <hr/> -->
        <b-table
          id="event-list-table"
          striped
          hover
          show-empty
          :items="events"
          :fields="fields"
          primary-key="id"
          :filter="filter"
          :busy="isLoading"
          :per-page="perPage"
          :current-page="currentPage"
        >
          <div
            slot="table-busy"
            class="text-center text-danger my-2"
          >
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>

          <template
            slot="title"
            slot-scope="row"
          >
            <b-link :to="'/event/' + row.item.id">
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

        <b-col cols="12">
          <div class="mt-3">
            <b-pagination
              v-model="currentPage"
              :total-rows="rows"
              :per-page="perPage"
              align="center"
              aria-controls="event-list-table"
            />
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
const fields = [
  { key: 'title', sortable: false },
  { key: 'start_time', sortable: true },
  { key: 'host_display_info', label: 'Host', sortable: true },
  { key: 'actions' }
]

export default {
  data () {
    return {
      isLoading: false,
      filter: null,
      fields,
      events: [],
      perPage: 10,
      currentPage: 1
    }
  },
  mounted () {
    this.isLoading = true
    this.axios.get('/api/event/')
      .then(res => {
        this.isLoading = false
        this.events = res.data
        console.log(res.data)
      })
      .catch(err => {
        this.isLoading = false
        console.log('failed to fetch events\n', err)
      })
  },
  computed: {
    rows () {
      return this.events.length
    }
  }
}
</script>
