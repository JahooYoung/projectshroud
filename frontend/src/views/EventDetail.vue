<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col col="12">
          <b-tabs pills vertical nav-wrapper-class="col-2 event-detail-sidebar">
            <b-tab title="Info" active>
              <b-row>
                <b-col md="8">
                  <b-form>
                    <b-form-group
                      id="titleInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Title"
                      label-for="titleInput"
                    >
                      <b-form-input id="titleInput" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="descriptionInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Description"
                      label-for="descriptionInput"
                    >
                      <b-form-textarea rows="8" id="descriptionInput" required></b-form-textarea>
                    </b-form-group>
                    <b-form-group
                      id="startTimeInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Start time"
                      label-for="startTimeInput"
                    >
                      <b-form-input id="startTimeInput" type="datetime-local" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="endTimeInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="End time"
                      label-for="endTimeInput"
                    >
                      <b-form-input id="endTimeInput" type="datetime-local" required></b-form-input>
                    </b-form-group>
                    <b-form-group
                      id="locationInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Location"
                      label-for="locationInput"
                    >
                      <b-form-input id="locationInput" type="datetime-local" required></b-form-input>
                    </b-form-group>

                    <b-form-group
                      id="publicInputGroup"
                      label-cols-sm="4"
                      label-cols-lg="3"
                      label="Public"
                      label-for="publicInput"
                    >
                      <div style="text-align: left;">
                        <b-form-checkbox size="lg" v-model="checked" name="check-button" switch>
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
                        <b-form-checkbox size="lg" v-model="checked" name="check-button" switch>
                        </b-form-checkbox>
                      </div>
                    </b-form-group>

                    <b-button variant="primary" href="#">Save</b-button>
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
export default {
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
    this.isLoading = true
    this.axios.get('/api/event/' + this.$route.params.id)
      .then(res => {
        this.isLoading = false
        // this.events = [];
        // for (let i = 0; i < 100; i++) {
        //   this.events = [...this.events, res.data];
        // }
        this.events = [res.data]
        this.form = res.data
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

<style>
.event-detail-sidebar {
  position: sticky;
  top: 4rem;
  z-index: 1000;
  height: calc(100vh - 3rem);
  padding-right: 1px;
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  /* border-bottom: 1px solid rgba(0,0,0,.1); */
  order: 0;
}
</style>
