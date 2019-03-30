<template>
  <div class="home">
    <b-jumbotron v-if="user === null" fluid container-fluid bg-variant="light">
      <template slot="header">Academic Conference</template>

      <template slot="lead">
        This is a simple hero unit, a simple jumbotron-style component for calling extra attention to
        featured content or information.
      </template>

      <hr class="my-4">

      <p>
        It uses utility classes for typography and spacing to space content out within the larger
        container.
      </p>

      <b-button variant="primary" to="/login">Login or Register</b-button>
      <!-- <b-button variant="success" href="#">I am host</b-button> -->
    </b-jumbotron>

    <b-container v-if="user !== null">
      <b-row>
        <b-col cols="4">
          <h3>Recent Events</h3>
          <b-list-group>
            <b-list-group-item
              v-for="event in events"
              :key="'recent-event-' + event.id"
              :to="`/event/${event.id}`"
              class="flex-column align-items-start"
            >
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">{{ event.title }}</h5>
                <small>{{ (new Date(event.start_time)).toLocaleDateString() }}</small>
              </div>

              <p class="mb-1">
              </p>

              <small>{{ event.location }} -- {{ event.host_display_info }}</small>
            </b-list-group-item>

          </b-list-group>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import { mapState } from 'vuex'

export default {
  name: 'home',
  data () {
    return {
      events: []
    }
  },
  computed: mapState({
    user: 'user'
  }),
  mounted () {
    this.axios.get('api/event/future/')
      .then(res => {
        console.log(res.data)
        this.events = res.data
      })
  }
}
</script>
