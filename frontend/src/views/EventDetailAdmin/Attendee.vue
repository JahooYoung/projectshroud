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
      this.axios.get('/api/event/' + this.$router.id + '/attendee/')
        .then(res => {
          console.log(res)
          attendee = res.data
        })
    }
  }
}
</script>
