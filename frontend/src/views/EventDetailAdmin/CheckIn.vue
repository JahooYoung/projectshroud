<template>
  <div>
    <b-button
      size="lg"
      :variant="checkingIn ? 'danger' : 'primary'"
      @click="onClick"
    >
      {{ checkingIn ? 'Stop' : 'Start'}} Check In
    </b-button>
    <b-img
      v-if="checkingIn"
      center
      style="margin-top: 10px"
      height="500px"
      src="https://picsum.photos/125/125/?image=58"
      alt="Center image"
    ></b-img>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoading: false,
      checkingIn: false,
      checkinToken: null,
    }
  },
  mounted () {
    this.refresh()
  },
  methods: {
    onClick () {
      if (this.checkingIn) {
        this.isLoading = true
        this.axios.delete(`api/checkin/${this.checkinToken}/stop/`)
          .then(res => {
            this.isLoading = false
            console.log(res)
            if (res.status < 300) {
              this.checkingIn = false
            } else {
              alert('failed to stop check in')
            }
          })
          .catch(err => {
            alert('failed to stop check in')
            console.log(err)
          })
      } else {
        this.isLoading = true
        this.axios.post('api/checkin/start/', {
          event_id: this.$route.params.id
        })
          .then(res => {
            this.isLoading = false
            console.log(res.data)
            if (res.status === 201) {
              this.checkingIn = true
              this.checkinToken = res.data.checkin_token
            } else {
              alert('failed to start check in')
            }
          })
          .catch(err => {
            alert('failed to start check in')
            console.log(err)
          })
      }
    },
    refresh () {
      this.isLoading = true
      this.axios.get(`api/event/${this.$route.params.id}/checkin/`)
        .then(res => {
          this.isLoading = false
          console.log(res.data)
          if (res.status === 200) {
            this.checkingIn = true
            this.checkinToken = res.data.checkin_token
          }
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to fetch events\n', err)
        })
    }
  }
}
</script>
