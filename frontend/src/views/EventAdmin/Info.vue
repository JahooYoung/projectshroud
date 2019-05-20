<template>
  <b-row>
    <b-col md="8">
      <b-form-group
        id="titleInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="Title"
        label-for="titleInput"
      >
        <b-form-input
          id="titleInput"
          v-model="event.title"
          required
        />
      </b-form-group>
      <b-form-group
        id="startTimeInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="Start time"
        label-for="startTimeInput"
      >
        <time-picker
          id="startTimeInput"
          v-model="event.startTime"
        />
      </b-form-group>
      <b-form-group
        id="endTimeInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="End time"
        label-for="endTimeInput"
      >
        <time-picker
          id="endTimeInput"
          v-model="event.endTime"
        />
      </b-form-group>
      <b-form-group
        id="locationInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="Location"
        label-for="locationInput"
      >
        <location-input
          id="locationInput"
          v-model="event.location"
        />
      </b-form-group>

      <b-form-group
        id="publicInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="Public"
        label-for="publicInput"
      >
        <div style="text-align: left;">
          <b-form-checkbox
            v-model="event.public"
            size="lg"
            switch
          />
        </div>
      </b-form-group>

      <b-form-group
        id="publicInputGroup"
        label-cols-sm="4"
        label-cols-lg="3"
        label="Require approve"
        label-for="publicInput"
      >
        <div style="text-align: left;">
          <b-form-checkbox
            v-model="event.requireApprove"
            size="lg"
            switch
          />
        </div>
      </b-form-group>

      <b-button
        variant="primary"
        :disabled="isLoading"
        @click="onSubmit"
      >
        <b-spinner
          v-show="isLoading"
          small
          type="grow"
        />
        {{ newEvent ? 'Create' : 'Save' }}
      </b-button>
    </b-col>
  </b-row>
</template>

<script>
import TimePicker from '@/components/TimePicker.vue'
import LocationInput from '@/components/LocationInput.vue'

export default {
  name: 'EventAdminInfo',
  components: {
    TimePicker,
    LocationInput
  },
  props: {
    newEvent: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      event: {
        title: '',
        startTime: null,
        endTime: null,
        location: '',
        public: true,
        requireApprove: false
      }
    }
  },
  watch: {
    '$route': 'refresh'
  },
  created () {
    if (!this.newEvent) {
      this.refresh()
    }
  },
  methods: {
    async onSubmit () {
      if (this.newEvent) {
        const res = await this.axios.post('/api/event/', this.event)
        this.$router.push('/event/' + res.data.id)
      } else {
        const res = await this.axios.patch(`/api/event/${this.$route.params.id}/`, this.event)
        this.event = res.data
        this.toastSuccess(`Event "${res.data.title}" saved successfully`)
      }
    },
    async refresh () {
      const res = await this.axios.get(`/api/event/${this.$route.params.id}/`)
      this.event = res.data
    }
  }
}
</script>
