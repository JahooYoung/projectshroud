<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="2">
          <b-card
            bg-variant="light"
            class="event-detail-sidebar"
          >
            <b-nav
              vertical
              pills
              justified
            >
              <b-nav-item
                :active="$route.name === 'eventAdminInfo'"
                to="info"
              >
                Basic Info
              </b-nav-item>
              <b-nav-item
                :active="$route.name === 'eventAdminDescription'"
                to="description"
              >
                Description
              </b-nav-item>
              <b-nav-item
                :active="$route.name === 'eventAdminAdministrator'"
                to="administrator"
              >
                Administrator
              </b-nav-item>
              <b-nav-item
                :active="$route.name === 'eventAdminAttendee'"
                to="attendee"
              >
                Attendee
              </b-nav-item>
              <b-nav-item
                :active="$route.name === 'eventAdminCheckin'"
                to="checkin"
              >
                Checkin
              </b-nav-item>
              <b-button
                block
                class="my-4"
                variant="danger"
                @click="$bvModal.show('modal-delete')"
              >
                Delete
              </b-button>
              <hr>
              <b-button
                block
                variant="outline-dark"
                :to="`/event/${$route.params.id}`"
              >
                Back
              </b-button>
            </b-nav>
          </b-card>
        </b-col>
        <b-col cols="10">
          <transition
            name="fade"
            mode="out-in"
          >
            <router-view />
          </transition>
        </b-col>
      </b-row>
    </b-container>

    <b-modal
      id="modal-delete"
      title="Confirm Deletion"
      lazy
      @show="deleteInput = ''"
      @shown="$refs.deleteConfirmInput.focus()"
      @ok="deleteEvent"
    >
      <b-form @submit="deleteEvent">
        <b-form-input
          ref="deleteConfirmInput"
          v-model="deleteInput"
          :state="deleteInputState"
          :placeholder="`Enter '${confirmMessage}'`"
        />
        <b-form-text v-if="isLoading">
          Deleting... Hold on a minute please...
        </b-form-text>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'EventAdminLayout',
  data () {
    return {
      confirmMessage: 'I am sure',
      deleteInput: ''
    }
  },
  computed: {
    deleteInputState () {
      return this.deleteInput === this.confirmMessage
    }
  },
  methods: {
    deleteEvent (evt) {
      evt.preventDefault()
      if (!this.deleteInputState) {
        return
      }
      this.axios.delete(`/api/event/${this.$route.params.id}/`)
        .then(res => {
          this.$router.push('/admin-event')
        })
    }
  }
}
</script>

<style>
.event-detail-sidebar {
  position: sticky;
  top: 4rem;
  z-index: 500;
  height: calc(100vh - 5rem);
  /* padding-right: 1px; */
  /* border-right: 1px solid rgba(0, 0, 0, 0.1); */
  order: 0;
}
</style>
