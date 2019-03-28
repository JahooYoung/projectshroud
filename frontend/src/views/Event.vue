<template>
  <div>
    <b-container>
      <h2>Event List</h2>
      <b-row>
        <b-col md="6" class="my-1">
          <b-form-group label-cols-sm="3" label="Filter" class="mb-0">
            <b-input-group>
              <b-form-input v-model="filter" placeholder="Type to Search" />
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
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
        </b-table>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoading: false,
      filter: '',
      fields: {
        id: {
          // label: 'Id',
          sortable: true
        },
        title: {
          // label: '',
          sortable: false
        },
        description: {
          // label: '',
          sortable: false
        },
        start_time: {
          // label: '',
          sortable: true
        },
        host: {
          // label: '',
          sortable: true
        },
        registerd_attendee: {}
      },
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
