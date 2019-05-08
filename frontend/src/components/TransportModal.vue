<template>
  <b-modal
    ref="transport-modal"
    size="lg"
    title="Edit Transport Info"
    :ok-title="id ? 'Save' : 'Create'"
    no-close-on-backdrop
    @ok="callback && callback(true)"
    @hide="callback && callback(false)"
  >
    <b-form-group
      label="Transport type:"
      label-for="transport-modal-input-2"
      label-cols-lg="3"
    >
      <b-form-select
        id="transport-modal-input-2"
        v-model="transport.transport_type"
        :options="transport_options"
      />
    </b-form-group>

    <b-form-group
      label="Transport id:"
      label-for="transport-modal-input-3"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-3"
        v-model="transport.transport_id"
        placeholder="Flight No. or Train No."
      />
    </b-form-group>

    <b-form-group
      label="Depart station:"
      label-for="transport-modal-input-4"
      label-cols-lg="3"
    >
      <location-input
        id="transport-modal-input-4"
        v-model="transport.depart_station"
        :type="transport.transport_type"
      />
    </b-form-group>

    <b-form-group
      label="Depart time:"
      label-for="transport-modal-input-5"
      label-cols-lg="3"
    >
      <flat-pickr
        id="transport-modal-input-5"
        v-model="transport.depart_time"
        class="form-control"
        :config="{ enableTime: true, time_24hr: true }"
      />
    </b-form-group>

    <b-form-group
      label="Arrival station:"
      label-for="transport-modal-input-6"
      label-cols-lg="3"
    >
      <location-input
        id="transport-modal-input-6"
        v-model="transport.arrival_station"
        :type="transport.transport_type"
      />
    </b-form-group>

    <b-form-group
      label="Arrival time:"
      label-for="transport-modal-input-7"
      label-cols-lg="3"
    >
      <flat-pickr
        id="transport-modal-input-7"
        v-model="transport.arrival_time"
        class="form-control"
        :config="{ enableTime: true, time_24hr: true }"
      />
    </b-form-group>

    <b-form-group
      label="Other detail:"
      label-for="transport-modal-input-8"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-8"
        v-model="transport.other_detail"
        placeholder="Enter other detail"
      />
    </b-form-group>
  </b-modal>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import LocationInput from '@/components/LocationInput.vue'

export default {
  name: 'TransportModal',
  components: {
    flatPickr,
    LocationInput
  },
  data () {
    return {
      id: null,
      transport: null,
      transport_options: [
        { value: 'Flight', text: '航班' },
        { value: 'Train', text: '列车' },
        { value: 'Other', text: '其他' }
      ],
      callback: null
    }
  },
  created () {
    this.reset()
  },
  methods: {
    reset () {
      this.transport = {
        user_id: undefined,
        event_id: null,
        transport_type: 'Flight',
        transport_id: '',
        depart_station: '',
        depart_time: null,
        arrival_station: '',
        arrival_time: null,
        other_detail: ''
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
          throw new Error('eventId is not provided')
        }
        try {
          const res = await this.axios.post(`/api/trans/`, {
            ...this.transport,
            depart_time: new Date(this.transport.depart_time),
            arrival_time: new Date(this.transport.arrival_time),
            event_id: eventId,
            user_id: userId || undefined
          })
          return res.data
        } catch (err) {
          if (err.response && err.response.status === 400) {
            this.$root.$bvToast.toast('Failed to save transport info', {
              title: 'Error',
              variant: 'danger',
              autoHideDelay: 4000,
              solid: true
            })
          }
        }
      } else {
        try {
          const res = await this.axios.put(`/api/trans/${this.id}/`, {
            ...this.transport,
            depart_time: new Date(this.transport.depart_time),
            arrival_time: new Date(this.transport.arrival_time)
          })
          return res.data
        } catch (err) {
          if (err.response && (err.response.status === 400 || err.response.status === 404)) {
            this.$root.$bvToast.toast('Failed to save transport info', {
              title: 'Error',
              variant: 'danger',
              autoHideDelay: 4000,
              solid: true
            })
          }
        }
      }
    },
    resetShow (...args) {
      this.reset()
      return this.show(...args)
    }
  }
}
</script>

<style>

</style>
