<template>
  <div>
    <b-container>
      <h2>Event List</h2>
      <b-row>
        <b-table striped hover :items="events" />
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      events: []
    }
  },
  mounted () {
    this.axios.get('/api/event/')
      .then(res => {
        this.events = res.data
      })
      .catch(err => {
        console.log('failed to fetch events\n', err)
      })
    this.axios.get('/api/event/1/')
      .then(res => {
        console.log(res.data)
      })
      .catch(err => {
        console.log('failed to fetch event 1\n', err)
      })
  }
}
</script>
