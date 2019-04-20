<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="12">
          <b-tabs lazy pills vertical nav-wrapper-class="col-2 event-detail-sidebar">
            <b-tab title="Info" active>
              <Info :newEvent="newEvent"/>
            </b-tab>
            <b-tab title="Administrator" :disabled="newEvent">
              <Administrator/>
            </b-tab>
            <b-tab title="Attendee" :disabled="newEvent">
              <Attendee/>
            </b-tab>
            <b-tab title="Checkin" :disabled="newEvent">
              <CheckIn/>
            </b-tab>
          </b-tabs>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Info from './Info'
import Administrator from './Administrator'
import Attendee from './Attendee'
import CheckIn from './CheckIn'

export default {
  name: 'EventDetailAdmin',
  props: ['newEvent'],
  components: {
    Info,
    Attendee,
    CheckIn,
    Administrator
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
