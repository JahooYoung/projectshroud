<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col col="12">
          <b-card no-body>
            <b-tabs pills card vertical nav-wrapper-class="col-2">
              <b-tab title="Info" active>
                <h2>Event Detail</h2>
                <b-table striped hover :busy="isLoading" :items="events" :fields="fields" primary-key="id">
                  <div slot="table-busy" class="text-center text-danger my-2">
                    <b-spinner class="align-middle" />
                    <strong>Loading...</strong>
                  </div>
                  <template slot="id" slot-scope="row">
                    <b-link :to="'/event/' + row.value">{{ row.value }}</b-link>
                  </template>
                </b-table>
              </b-tab>
              <b-tab title="Attendee">

              </b-tab>
              <b-tab title="Utility">

              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <!-- <b-col col="12" md="2">
          <nav>
            <b-nav tabs pills sticky vertical class="sidebar">
              <b-nav-item active>Active</b-nav-item>
              <b-nav-item>Link</b-nav-item>
              <b-nav-item>Another Link</b-nav-item>
              <b-nav-item disabled>Disabled</b-nav-item>
            </b-nav>
          </nav>
        </b-col>
        <b-col col="12" md="10">
          <h2>Event Detail</h2>
          <b-table striped hover :busy="isLoading" :items="events" :fields="fields" primary-key="id">
            <div slot="table-busy" class="text-center text-danger my-2">
              <b-spinner class="align-middle" />
              <strong>Loading...</strong>
            </div>
            <template slot="id" slot-scope="row">
              <b-link :to="'/event/' + row.value">{{ row.value }}</b-link>
            </template>
          </b-table>
        </b-col> -->
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
        registered_attendee: {}
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

<style scoped>
.sidebar {
  position: sticky;
  top: 4rem;
  z-index: 1000;
  height: calc(100vh - 4rem);
  padding-right: 1px;
  border-right: 1px solid rgba(0,0,0,.1);
  border-bottom: 1px solid rgba(0,0,0,.1);
  order: 0;
}
</style>
