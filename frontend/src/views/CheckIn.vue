<template>
  <div style="padding-top: 13rem;">
    <h4 class="mb-3">
      <font-awesome-icon
        v-if="checked"
        :icon="['far', 'check-circle']"
        :style="{ color: 'green' }"
      />
      <font-awesome-icon
        v-else
        :icon="['far', 'times-circle']"
        :style="{ color: 'red' }"
      />
      {{ msg }}
    </h4>
    <hr class="mb-5">
    <div class="pt-3">
      <b-button
        v-if="!checked"
        variant="danger"
        :disabled="isLoading"
        @click="checkin"
      >
        Try to checkin again
      </b-button>
    </div>
    <div class="pt-4">
      <b-button
        variant="dark"
        :disabled="isLoading"
        :to="`/event/${$route.query.id}`"
      >
        Return to event info
      </b-button>
    </div>
  </div>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimesCircle, faCheckCircle } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimesCircle, faCheckCircle)

export default {
  name: 'UserCheckIn',
  components: {
    FontAwesomeIcon
  },
  data () {
    return {
      msg: 'Processing',
      checked: false
    }
  },
  created () {
    this.checkin()
  },
  methods: {
    checkin () {
      if (!this.checkActivated()) {
        return
      }
      this.msg = 'Checking in...'
      const token = this.$route.query.token
      this.axios.get(`/api/checkin/${token}/`)
        .then(res => this.axios.post(`/api/checkin/${token}/`))
        .then(res => {
          this.msg = 'Checkin successfully'
          this.checked = true
        })
        .catch(err => {
          this.msg = null
          if (err.response) {
            switch (err.response.status) {
              case 400:
                this.msg = err.response.data[0]
                if (this.msg === 'Already checked in.') {
                  this.checked = true
                }
                break
              case 404:
                this.msg = 'Please scan the QRcode again'
                break
            }
          }
          if (!this.msg) {
            this.msg = 'Failed to checkin'
          }
        })
    }
  }
}
</script>
