<template>
  <b-row>
    <b-col md="8">
      <b-form>
        <b-form-group
          id="titleInputGroup"
          label-cols-sm="4"
          label-cols-lg="3"
          label="Title"
          label-for="titleInput"
        >
          <b-form-input
            id="titleInput"
            v-model="form.title"
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
          <flat-pickr
            id="startTimeInput"
            v-model="form.startTime"
            class="form-control"
            :config="configs.start"
            @on-change="onStartChange"
          />
        </b-form-group>
        <b-form-group
          id="endTimeInputGroup"
          label-cols-sm="4"
          label-cols-lg="3"
          label="End time"
          label-for="endTimeInput"
        >
          <flat-pickr
            id="endTimeInput"
            v-model="form.endTime"
            class="form-control"
            :config="configs.end"
            @on-change="onEndChange"
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
            v-model="form.location"
            required
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
              v-model="form.public"
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
              v-model="form.requireApprove"
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
      </b-form>
    </b-col>
  </b-row>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import LocationInput from '@/components/LocationInput.vue'

export default {
  name: 'EventAdminInfo',
  components: {
    flatPickr,
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
      form: {
        title: '',
        startTime: null,
        endTime: null,
        location: '',
        public: false,
        requireApprove: false
      },
      event: null,
      configs: {
        start: {
          enableTime: true,
          time_24hr: true,
          maxDate: null
        },
        end: {
          enableTime: true,
          time_24hr: true,
          minDate: null
        }
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
    onStartChange (selectedDates, dateStr, instance) {
      this.$set(this.configs.end, 'minDate', dateStr)
    },
    onEndChange (selectedDates, dateStr, instance) {
      this.$set(this.configs.start, 'maxDate', dateStr)
    },
    updateForm (data) {
      this.event = data
      this.form.title = data.title
      this.form.startTime = data.start_time
      this.form.endTime = data.end_time
      this.form.location = data.location
      this.form.public = data.public
      this.form.requireApprove = data.require_approve
    },
    onSubmit (evt) {
      evt.preventDefault()
      const data = {
        title: this.form.title,
        description: this.event ? this.event.description : '',
        description_html: this.event ? this.event.description_html : '',
        start_time: new Date(this.form.startTime),
        end_time: new Date(this.form.endTime),
        location: this.form.location,
        public: this.form.public,
        require_approve: this.form.requireApprove
      }
      if (this.newEvent) {
        this.axios.post('/api/event/', data)
          .then(res => {
            this.$router.push('/event/' + res.data.id)
          })
      } else {
        this.axios.put(`/api/event/${this.$route.params.id}/`, data)
          .then(res => {
            this.$bvToast.toast(`Event "${res.data.title}" saved successfully`, {
              title: `Success`,
              autoHideDelay: 5000,
              solid: true
            })
            this.updateForm(res.data)
          })
      }
    },
    refresh () {
      this.axios.get(`/api/event/${this.$route.params.id}/`)
        .then(res => this.updateForm(res.data))
    }
  }
}
</script>
