<template>
  <div>
    <h2>Attendee List</h2>
    <b-table striped hover :items="attendee"></b-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoading: false,
      fields: [
        { key: '', label: '' }
      ],
      attendee: []
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/' + this.$route.params.id + '/attendee/')
        .then(res => {
          console.log(res)
          this.attendee = res.data
        })
    }
  }
}
</script>
