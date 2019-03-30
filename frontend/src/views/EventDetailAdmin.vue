<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="12">
          <b-tabs pills vertical nav-wrapper-class="col-2 event-detail-sidebar">
            <b-tab title="Info" active>
              <b-row>
                <b-col md="8">
                  <b-form @submit="onSubmit">
                    <b-form-group
                      id="titleInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Title"
                      label-for="titleInput"
                    >
                      <b-form-input v-model="form.title" id="titleInput" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="descriptionInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Description"
                      label-for="descriptionInput"
                    >
                      <b-form-textarea v-model="form.description" rows="8" id="descriptionInput" required></b-form-textarea>
                    </b-form-group>
                    <b-form-group
                      id="startTimeInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Start time"
                      label-for="startTimeInput"
                    >
                      <b-form-input v-model="form.startTime" id="startTimeInput" type="datetime-local" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="endTimeInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="End time"
                      label-for="endTimeInput"
                    >
                      <b-form-input v-model="form.endTime" id="endTimeInput" type="datetime-local" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="locationInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Location"
                      label-for="locationInput"
                    >
                      <b-form-input v-model="form.location" id="locationInput" required></b-form-input>
                    </b-form-group>

                    <b-form-group
                      id="publicInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Public"
                      label-for="publicInput"
                    >
                      <div style="text-align: left;">
                        <b-form-checkbox size="lg" v-model="form.public" switch>
                        </b-form-checkbox>
                      </div>
                    </b-form-group>

                    <b-form-group
                      id="publicInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Require approve"
                      label-for="publicInput"
                    >
                      <div style="text-align: left;">
                        <b-form-checkbox size="lg" v-model="form.requireApprove" switch>
                        </b-form-checkbox>
                      </div>
                    </b-form-group>

                    <b-button variant="primary" type="submit" :disable="isLoading">
                      <b-spinner small type="grow" v-show="isLoading"></b-spinner>
                      Save
                    </b-button>
                  </b-form>
                </b-col>
              </b-row>
            </b-tab>

            <b-tab title="Attendee"></b-tab>

            <b-tab title="Utility">
              <h2>Event Detail</h2>
              <b-table
                striped
                hover
                :busy="isLoading"
                :items="events"
                :fields="fields"
                primary-key="id"
              >
                <div slot="table-busy" class="text-center text-danger my-2">
                  <b-spinner class="align-middle"/>
                  <strong>Loading...</strong>
                </div>
                <template slot="id" slot-scope="row">
                  <b-link :to="'/event/' + row.value">{{ row.value }}</b-link>
                </template>
              </b-table>
            </b-tab>
          </b-tabs>
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
        </b-col>-->
      </b-row>
    </b-container>
  </div>
</template>

<script>
function date2input (date) {
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  date.setSeconds(0, 0)
  date = date.toISOString()
  return date.substr(0, date.length - 1)
}

function input2date (str) {
  let date = new Date(str)
  return date
}

export default {
  name: 'EventDetailAdmin',
  data () {
    return {
      isLoading: false,
      fields: {
        id: { sortable: true },
        title: { sortable: false },
        description: { sortable: false },
        start_time: { sortable: true },
        host: { sortable: true },
        registered_attendee: {}
      },
      form: {
        title: '',
        description: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        requireApprove: false
      },
      events: []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    onSubmit (e) {
      console.log('OrzJahoo');
      e.preventDefault()
      this.isLoading = true
      this.axios.put('/api/event/' + this.$route.params.id + '/', {
        title: this.form.title,
        description: this.form.description,
        start_time: input2date(this.form.startTime).toISOString(),
        end_time: input2date(this.form.endTime).toISOString(),
        location: this.form.location,
        public: this.form.public,
        require_approve: this.form.requireApprove
      })
        .then(res => {
          if (res.status === 200) {
            this.refresh()
          }
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to update events\n', err)
        })
    },
    refresh () {
      this.isLoading = true
      this.axios.get('/api/event/' + this.$route.params.id)
        .then(res => {
          this.isLoading = false
          console.log(res.data)
          this.form.title = res.data.title
          this.form.description = res.data.description
          this.form.startTime = date2input(new Date(res.data.start_time))
          this.form.endTime = date2input(new Date(res.data.end_time))
          this.form.location = res.data.location
          this.form.public = res.data.public
          this.form.requireApprove = res.data.require_approve
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to fetch events\n', err)
        })
    }
  }
}
</script>

<style>
.event-detail-sidebar {
  position: sticky;
  top: 4rem;
  z-index: 1000;
  height: calc(100vh - 3rem);
  padding-right: 1px;
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  order: 0;
}
</style>
