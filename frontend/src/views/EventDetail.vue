<template>
  <div>
    <b-container>
      <h2>Event List</h2>
      <b-row>
        <b-table striped hover :busy="isLoading" :items="events" :fields="fields" primary-key="id">
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
    this.axios.get('/api/event/' + this.$route.params.id)
      .then(res => {
        this.isLoading = false
        this.events = [res.data]
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
