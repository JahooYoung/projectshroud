<template>
  <div>
    <b-container>
      <h2>Event List</h2>
      <b-row>
        <b-col md="4" class="my-1">
          <b-input-group>
            <b-input-group-text slot="prepend">Filter</b-input-group-text>
            <b-form-input v-model="filter" placeholder="Type to Search" />
            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-col>
        <b-col offset-md="6" md="2" class="my-1">
          <b-button variant="outline-info">New Event</b-button>
        </b-col>

        <b-table striped hover show-empty :busy="isLoading" :items="events"
          :fields="fields" primary-key="id" :filter="filter"
        >
          <div slot="table-busy" class="text-center text-danger my-2">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>

          <template slot="id" slot-scope="row">
            <b-link :to="'/event/' + row.value">{{ row.value }}</b-link>
          </template>

          <template slot="actions" slot-scope="row">
            <b-button size="sm" @click="row.toggleDetails">
              {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
            </b-button>
          </template>

          <template slot="row-details" slot-scope="row">
            <b-card>
              <ul>
                <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value }}</li>
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
  { key: 'id', sortable: true },
  { key: 'title', sortable: false },
  { key: 'start_time', sortable: true },
  { key: 'host', sortable: true },
  { key: 'actions' }
]

export default {
  data () {
    return {
      isLoading: false,
      filter: null,
      fields,
      events: []
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
    // this.axios.get('/api/event/1/')
    //   .then(res => {
    //     console.log(res.data)
    //   })
    //   .catch(err => {
    //     console.log('failed to fetch event 1\n', err)
    //   })
  }
}
</script>
