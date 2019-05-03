<template>
  <div>
    <b-jumbotron
      v-if="!user"
      fluid
      container-fluid
      header-level="4"
      bg-variant="white"
    >
      <template slot="header">
        Academic Conference
      </template>

      <template slot="lead">
        This is a simple hero unit, a simple jumbotron-style component for calling extra attention to
        featured content or information.
      </template>

      <hr class="my-4">

      <p>
        It uses utility classes for typography and spacing to space content out within the larger
        container.
      </p>

      <b-button
        variant="primary"
        to="/login"
      >
        Login or Register
      </b-button>
      <!-- <b-button variant="success" href="#">I am host</b-button> -->
    </b-jumbotron>

    <b-container v-else>
      <b-row>
        <b-col
          cols="12"
          order="2"
          lg="8"
          order-lg="1"
        >
          <h3>{{ $t('Recent Events') }}</h3>
          <b-card
            v-for="event in futureEvents"
            :key="'recent-event-' + event.id"
            no-body
            border-variant="white"
            class="my-4"
          >
            <div class="d-flex w-100 justify-content-between">
              <h4 class="mb-2">
                <b-link
                  :to="`/event/${event.id}`"
                  active-class=""
                  exact-active-class=""
                >
                  {{ event.title }}
                </b-link>
              </h4>
              <em>{{ event.location }}, {{ new Date(event.start_time).toLocaleDateString() }}</em>
            </div>
            <p
              class="mb-2"
              style="text-align: left"
            >
              Short description here?
            </p>
            <hr>
          </b-card>
        </b-col>

        <b-col
          cols="12"
          order="1"
          lg="4"
          order-lg="2"
          class="mb-3"
        >
          <b-card
            no-body
            :header="$t('Registered Future Events')"
            class="mb-3"
            border-variant="primary"
            header-bg-variant="primary"
            header-text-variant="white"
          >
            <b-list-group flush>
              <b-list-group-item
                v-for="event in registeredFutureEvents"
                :key="'recent-event-' + event.id"
                :to="'/event/' + event.id"
                class="d-flex justify-content-between align-items-center"
              >
                {{ event.title }}
                <small>{{ (new Date(event.start_time)).toLocaleDateString() }}</small>
              </b-list-group-item>
            </b-list-group>
          </b-card>
          <b-card
            no-body
            :header="$t('Manage Events')"
            border-variant="dark"
            header-bg-variant="dark"
            header-text-variant="white"
          >
            <b-list-group flush>
              <b-list-group-item
                v-for="event in manageEvents"
                :key="'recent-event-' + event.id"
                :to="'/event/' + event.id"
                class="d-flex justify-content-between align-items-center"
              >
                {{ event.title }}
                <b-badge
                  variant="dark"
                  pill
                >
                  14
                </b-badge>
              </b-list-group-item>
            </b-list-group>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      futureEvents: [],
      registeredFutureEvents: [],
      manageEvents: []
    }
  },
  created () {
    this.axios.get('/api/event/future/')
      .then(res => {
        this.futureEvents = res.data
      })
    if (!this.userActivated) {
      return
    }
    this.axios.get('/api/event/registered/future/')
      .then(res => {
        this.registeredFutureEvents = res.data.map(x => x.event_info)
      })
    this.axios.get('/api/event/admins/')
      .then(res => {
        this.manageEvents = res.data.map(x => x.event_info)
      })
  }
}
</script>
