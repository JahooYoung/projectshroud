<template>
  <div>
    <b-modal
      id="modal-countdown"
      ok-only
      ok-disabled
      no-close-on-esc
      no-close-on-backdrop
    >
      <template #modal-header>
        <h5>Activation succeeded</h5>
      </template>
      You have successfully activate your email. <br>
      This page will automatically close in <b>{{ countdown }}</b> seconds.
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'SendActivation',
  data () {
    return {
      countdown: 10
    }
  },
  mounted () {
    const token = this.$route.query.token
    this.axios.post(`/api/activate/`, {
      token
    })
      .then(res => {
        this.$bvModal.show('modal-countdown')
        setInterval(() => {
          if (--this.countdown === 0) {
            window.opener = null
            window.open('', '_self')
            window.close()
          }
        }, 1000)
      })
      .catch(err => err.response && alert(err.response.data))
  }
}
</script>
