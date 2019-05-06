<template>
  <div>
    <b-button
      size="lg"
      :variant="checkingIn ? 'danger' : 'primary'"
      :disabled="isLoading"
      @click="onClick"
    >
      <b-spinner
        v-show="isLoading"
        small
        type="grow"
      />
      {{ checkingIn ? 'Stop' : 'Start' }} Check In
    </b-button>
    <b-img
      v-if="checkingIn && qrcodeURL"
      center
      fluid
      :src="qrcodeURL"
      alt="Qrcode cannot display correctly"
    />
  </div>
</template>

<script>
export default {
  name: 'EventAdminCheckin',
  data () {
    return {
      checkingIn: false,
      checkinToken: null,
      qrcodeURL: null,
      location: window.location
    }
  },
  watch: {
    '$route': 'refresh'
  },
  created () {
    this.refresh()
  },
  methods: {
    onClick () {
      if (this.checkingIn) {
        this.qrcodeURL = null
        this.axios.delete(`/api/checkin/${this.checkinToken}/stop/`)
          .then(res => {
            this.checkingIn = false
          })
      } else {
        this.axios.post('/api/checkin/start/', {
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
      this.axios.get(`/api/event/${this.$route.params.id}/checkin/`)
        .then(res => {
          this.checkingIn = true
          this.checkinToken = res.data.checkin_token
          this.getQrcode()
        })
    },
    getQrcode () {
      const url = `${this.location.origin}/checkin/?token=${this.checkinToken}&id=${this.$route.params.id}`
      console.log(url)
      this.axios.post('/api/qrcode/', {
        text: url
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
