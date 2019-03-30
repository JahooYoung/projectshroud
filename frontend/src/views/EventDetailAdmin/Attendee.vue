<template>
  <div>
    <h2>Attendee List</h2>
    <b-container>
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
        <b-col offset-md="3" md="1" class="my-1">
          <b-button variant="outline-info" href="#">Export</b-button>
        </b-col>
        <b-col offset-md="0" md="2" class="my-1">
          <b-button variant="outline-info" href="#">Add attendee</b-button>
        </b-col>
        <b-col offset-md="0" md="1" class="my-1">
          <b-button variant="outline-info" @click="refresh" :disabled="isLoading">Refresh</b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table
      striped
      hover
      show-empty
      :fields="fields"
      primary-key="userprofile.id"
      :items="attendee"
      :busy="isLoading"
      :filter="filter"
    >
      <div slot="table-busy" class="text-center text-danger my-2">
        <b-spinner class="align-middle" />
        <strong>Loading...</strong>
      </div>

      <template slot="checked_in" slot-scope="row">
        <font-awesome-icon v-if="row.value" :id="'checkin-popover-' + row.item.userprofile.id" icon="check-circle"/>
        <font-awesome-icon v-else :id="'checkin-popover-' + row.item.userprofile.id" icon="times-circle"/>
        <b-popover :target="'checkin-popover-' + row.item.userprofile.id" triggers="hover focus">
          <template slot="title">Manually check in (click to keep)</template>
          <b-button variant="success" @click="1" :disabled="row.value">Manually check in</b-button>
        </b-popover>
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
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoading: false,
      fields: [
        { key: 'userprofile.real_name', label: 'Name' },
        { key: 'userprofile.mobile', label: 'Mobile' },
        { key: 'date_registered', label: 'Registered Time' },
        { key: 'transport', label: 'Arrive Time' },
        { key: 'checked_in', label: 'Checked in' }
      ],
      filter: null,
      attendee: []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.isLoading = true
      this.axios.get('/api/event/' + this.$route.params.id + '/attendee/')
        .then(res => {
          this.isLoading = false
          console.log(res)
          this.attendee = res.data
        })
        .catch(err => {
          this.isLoading = false
          console.log(err)
        })
    }
  }
}
</script>
