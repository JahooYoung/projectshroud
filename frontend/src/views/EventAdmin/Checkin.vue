<template>
  <div>
    <b-button
      size="lg"
      :variant="checkingIn ? 'danger' : 'primary'"
      :disabled="isLoading"
      @click="onClick"
    >
      <b-spinner
        small
        type="grow"
        v-show="isLoading"
      />
      {{ checkingIn ? 'Stop' : 'Start' }} Check In
    </b-button>
    <b-img
      v-if="checkingIn && qrcodeURL"
      center
      style="margin-top: 10px"
      height="500px"
      :src="qrcodeURL"
      alt="Center image"
    />
  </div>
</template>

<script>
export default {
  data () {
    return {
      checkingIn: false,
      checkinToken: null,
      qrcodeURL: null,
      location: window.location
    }
  },
  created () {
    this.refresh()
  },
  watch: {
    '$route': 'refresh'
  },
  methods: {
    onClick () {
      if (this.checkingIn) {
        this.qrcodeURL = null
        this.axios.delete(`api/checkin/${this.checkinToken}/stop/`)
          .then(res => {
            this.checkingIn = false
          })
      } else {
        this.axios.post('api/checkin/start/', {
          event_id: this.$route.params.id
        })
          .then(res => {
            this.checkingIn = true
            this.checkinToken = res.data.checkin_token
            this.getQrcode()
          })
      }
    },
    refresh () {
      this.axios.get(`api/event/${this.$route.params.id}/checkin/`)
        .then(res => {
          this.checkingIn = true
          this.checkinToken = res.data.checkin_token
          this.getQrcode()
        })
    },
    getQrcode () {
      this.axios.post('/api/qrcode/', {
        text: `http://${this.location.host}/#/checkin/${this.checkinToken}`
      }, {
        responseType: 'blob'
      })
        .then(res => {
          const qrcode = new Blob([res.data], { type: 'image/png' })
          this.qrcodeURL = URL.createObjectURL(qrcode)
        })
    }
  }
}
</script>
