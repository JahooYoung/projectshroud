<template>
  <b-modal
    ref="transport-modal"
    size="lg"
    :title="$t('Edit Transport Info')"
    :ok-title="id ? $t('Save') : $t('Create')"
    no-close-on-backdrop
    @ok="callback && callback(true)"
    @hide="callback && callback(false)"
  >
    <b-form-group
      :label="$t('Transport type:')"
      label-for="transport-modal-input-2"
      label-cols-lg="3"
    >
      <b-form-select
        id="transport-modal-input-2"
        v-model="transport.transportType"
        :options="transportOptions"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Transport id:')"
      label-for="transport-modal-input-3"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-3"
        v-model="transport.transportId"
        :placeholder="$t('Flight No. or Train No.')"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Depart station:')"
      label-for="transport-modal-input-4"
      label-cols-lg="3"
    >
      <location-input
        id="transport-modal-input-4"
        v-model="transport.departStation"
        :type="transport.transportType"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Depart time:')"
      label-for="transport-modal-input-5"
      label-cols-lg="3"
    >
      <time-picker
        id="transport-modal-input-5"
        v-model="transport.departTime"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Arrival station:')"
      label-for="transport-modal-input-6"
      label-cols-lg="3"
    >
      <location-input
        id="transport-modal-input-6"
        v-model="transport.arrivalStation"
        :type="transport.transportType"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Arrival time:')"
      label-for="transport-modal-input-7"
      label-cols-lg="3"
    >
      <time-picker
        id="transport-modal-input-7"
        v-model="transport.arrivalTime"
      />
    </b-form-group>

    <b-form-group
      :label="$t('Other detail:')"
      label-for="transport-modal-input-8"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-8"
        v-model="transport.otherDetail"
        :placeholder="$t('Enter other detail')"
      />
    </b-form-group>
  </b-modal>
</template>

<script>
import TimePicker from '@/components/TimePicker.vue'
import LocationInput from '@/components/LocationInput.vue'
import { loadLanguageAsync } from '@/plugins/i18n'

export default {
  name: 'TransportModal',
  components: {
    TimePicker,
    LocationInput
  },
  data () {
    return {
      id: null,
      transport: null,
      transportOptions: Object.freeze([
        { value: 'Flight', text: this.$t('Flight') },
        { value: 'Train', text: this.$t('Train') },
        { value: 'Other', text: this.$t('Other') }
      ]),
      callback: null
    }
  },
  created () {
    this.reset()
  },
  methods: {
    reset () {
      this.transport = {
        eventId: null,
        transportType: this.$t('Flight'),
        transportId: '',
        departStation: '',
        departTime: null,
        arrivalStation: '',
        arrivalTime: null,
        otherDetail: ''
      }
    },
    showModal () {
      return new Promise(resolve => {
        this.callback = value => {
          this.callback = null
          resolve(value)
        }
        this.$refs['transport-modal'].show()
      })
    },
    async show (dataOrId, eventId, userId) {
      if (typeof dataOrId === 'object' && dataOrId) {
        const data = dataOrId
        for (let key in this.transport) {
          this.transport[key] = data[key]
        }
        this.id = data.id
      } else if (typeof dataOrId === 'number') {
        this.id = dataOrId
        const res = await this.axios.get(`/api/trans/${this.id}/`)
        for (let key in this.transport) {
          this.transport[key] = res.data[key]
        }
      } else {
        this.id = null
      }

      if (!await this.showModal()) {
        return false
      }

      if (!this.id) {
        if (!eventId) {
          throw new Error(this.$t('eventId is not provided'))
        }
        try {
          const res = await this.axios.post(`/api/trans/`, {
            ...this.transport,
            eventId,
            userId
          })
          return res.data
        } catch (err) {
          if (err.response) {
            this.toastError(this.$t('Failed to save transport info'))
          }
        }
      } else {
        try {
          const res = await this.axios.put(`/api/trans/${this.id}/`, this.transport)
          return res.data
        } catch (err) {
          if (err.response) {
            this.toastError(this.$t('Failed to save transport info'))
          }
        }
      }
    },
    resetShow (...args) {
      this.reset()
      return this.show(...args)
    },
    changeLocale (lang) {
      loadLanguageAsync(lang)
    }
  }
}
</script>

<style>

</style>
