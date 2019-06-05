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
        v-model="transport.transportType"
        :options="transportOptions"
      />
    </b-form-group>

    <b-form-group
      label="Transport id:"
      label-for="transport-modal-input-3"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-3"
        v-model="transport.transportId"
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
        v-model="transport.departStation"
        :type="transport.transportType"
      />
    </b-form-group>

    <b-form-group
      label="Depart time:"
      label-for="transport-modal-input-5"
      label-cols-lg="3"
    >
      <time-picker
        id="transport-modal-input-5"
        v-model="transport.departTime"
      />
    </b-form-group>

    <b-form-group
      label="Arrival station:"
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
      label="Arrival time:"
      label-for="transport-modal-input-7"
      label-cols-lg="3"
    >
      <time-picker
        id="transport-modal-input-7"
        v-model="transport.arrivalTime"
      />
    </b-form-group>

    <b-form-group
      label="Other detail:"
      label-for="transport-modal-input-8"
      label-cols-lg="3"
    >
      <b-form-input
        id="transport-modal-input-8"
        v-model="transport.otherDetail"
        placeholder="Enter other detail"
      />
    </b-form-group>
  </b-modal>
</template>

<script>
import { BFormGroup, BFormInput, BFormSelect } from 'bootstrap-vue'
import TimePicker from '@/components/TimePicker.vue'
import LocationInput from '@/components/LocationInput.vue'

const transportOptions = Object.freeze([
  { value: 'Flight', text: '航班' },
  { value: 'Train', text: '列车' },
  { value: 'Other', text: '其他' }
])

export default {
  name: 'TransportModal',
  components: {
    TimePicker,
    LocationInput,
    BFormGroup,
    BFormInput,
    BFormSelect
  },
  data () {
    return {
      id: null,
      transport: null,
      transportOptions,
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
        transportType: 'Flight',
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
          throw new Error('eventId is not provided')
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
            this.toastError('Failed to save transport info')
          }
        }
      } else {
        try {
          const res = await this.axios.put(`/api/trans/${this.id}/`, this.transport)
          return res.data
        } catch (err) {
          if (err.response) {
            this.toastError('Failed to save transport info')
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
