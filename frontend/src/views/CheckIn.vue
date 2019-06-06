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
      {{ $t('CheckIn.vue msg',[msg]) }}
    </h4>
    <hr class="mb-5">
    <div class="pt-3">
      <b-button
        v-if="!checked"
        variant="danger"
        :disabled="isLoading"
        @click="checkin"
      >
        {{ $t('Try to checkin again') }}
      </b-button>
    </div>
    <div class="pt-4">
      <b-button
        variant="dark"
        :disabled="isLoading"
        :to="`/event/${$route.query.id}`"
      >
        {{ $t('Return to event info') }}
      </b-button>
    </div>
  </div>
</template>

<script>
import { BButton } from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimesCircle, faCheckCircle } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimesCircle, faCheckCircle)

export default {
  name: 'UserCheckIn',
  components: {
    FontAwesomeIcon,
    BButton
  },
  data () {
    return {
      checked: false,
      msg: this.$t('Processing...')
    }
  },
  created () {
    this.checkin()
  },
  methods: {
    async checkin () {
      if (!this.checkActivated()) {
        return
      }
      this.msg = this.$t('Checking in...')
      const token = this.$route.query.token
      try {
        await this.axios.post(`/api/checkin/${token}/`)
        this.msg = this.$t('Checkin successfully.')
        this.checked = true
      } catch (err) {
        this.msg = this.$t('Failed to checkin.')
        if (err.response) {
          switch (err.response.status) {
            case 400:
              this.msg = this.$t(err.response.data[0])
              if (this.msg === this.$t('Already checked in.')) {
                this.checked = true
              }
              break
            case 404:
              this.msg = this.$t('Channel not found.')
              break
          }
        }
      }
    }
  }
}
</script>
