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
              <hr>
              <b-button
                style="vertical-align: center"
                block
                variant="danger"
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
  </div>
</template>

<script>
export default {
  name: 'EventAdminLayout'
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
