<template>
  <div>
    <b-modal
      id="modal-success"
      ok-only
      ok-title="Close Now"
      no-close-on-esc
      no-close-on-backdrop
      centered
      @ok="close"
    >
      <template #modal-header>
        <h5>{{ $t('Activation succeeded') }}</h5>
      </template>
      {{ $t('You have successfully activate your email.') }} <br>
      <p :v-html="$t('This page will automatically close in <b></b> seconds.',[countdown])" />
    </b-modal>
    <b-modal
      id="modal-error"
      centered
      :ok-title="$t('Retry')"
      ok-variant="danger"
      :cancel-title="$t('Close Tab')"
      cancel-variant="dark"
      no-close-on-esc
      no-close-on-backdrop
      @ok="activate"
      @cancel.prevent="close"
    >
      <template #modal-header>
        <h5>{{ $t('Activation failed') }}</h5>
      </template>
      {{ $t('SendActivation.vue msg',[msg]) }}
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
  computed: {
    msg () {
      return this.$t('Some error occured...')
    }
  },
  mounted () {
    this.$store.commit('clearUserToken')
    this.activate()
  },
  methods: {
    activate () {
      const token = this.$route.query.token
      this.axios.post(`/api/activate/`, {
        token
      })
        .then(res => {
          this.$bvModal.show('modal-success')
          setInterval(() => {
            if (--this.countdown === 0) {
              this.close()
            }
          }, 1000)
        })
        .catch(err => {
          if (err.response) {
            this.msg = err.response.data[0]
          }
          this.$bvModal.show('modal-error')
        })
    },
    close () {
      window.opener = null
      window.open('', '_self')
      window.close()
    }
  }
}
</script>
