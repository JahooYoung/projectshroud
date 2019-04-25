<template>
  <b-row>
    <b-col md="8">
      <b-form @submit="onSubmit">
        <b-form-group
          id="titleInputGroup"
          label-cols-sm="4"
          label-cols-lg="3"
          label="Title"
          label-for="titleInput"
        >
          <b-form-input
            v-model="form.title"
            id="titleInput"
            required
          />
        </b-form-group>
        <b-form-group
          id="descriptionInputGroup"
          label-cols-sm="4"
          label-cols-lg="3"
          label="Description"
          label-for="descriptionInput"
        >
          <b-form-textarea
            v-model="form.description"
            rows="8"
            id="descriptionInput"
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
          <!-- <b-form-input
            v-model="form.startTime"
            id="startTimeInput"
            type="datetime-local"
            required
          /> -->
          <flat-pickr
            class="form-control"
            id="startTimeInput"
            :config="configs.start"
            v-model="form.startTime"
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
          <!-- <b-form-input
            v-model="form.endTime"
            id="endTimeInput"
            type="datetime-local"
            required
          /> -->
          <flat-pickr
            class="form-control"
            id="endTimeInput"
            :config="configs.end"
            v-model="form.endTime"
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
          <b-form-input
            v-model="form.location"
            id="locationInput"
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
              size="lg"
              v-model="form.public"
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
              size="lg"
              v-model="form.requireApprove"
              switch
            />
          </div>
        </b-form-group>

        <b-button
          variant="primary"
          type="submit"
          :disabled="isLoading"
        >
          <b-spinner
            small
            type="grow"
            v-show="isLoading"
          />
          {{ buttonName }}
        </b-button>
      </b-form>
    </b-col>
  </b-row>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  name: 'Info',
  components: {
    flatPickr
  },
  props: {
    newEvent: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      buttonName: 'Save',
      form: {
        title: '',
        description: '',
        startTime: null,
        endTime: null,
        location: '',
        public: false,
        requireApprove: false
      },
      configs: {
        start: {
          enableTime: true,
          maxDate: null
        },
        end: {
          enableTime: true,
          minDate: null
        }
      }
    }
  },
  created () {
    if (this.newEvent) {
      this.buttonName = 'Create'
    } else {
      this.refresh()
    }
  },
  watch: {
    '$route': 'refresh'
  },
  methods: {
    onStartChange (selectedDates, dateStr, instance) {
      this.$set(this.configs.end, 'minDate', dateStr)
    },
    onEndChange (selectedDates, dateStr, instance) {
      this.$set(this.configs.start, 'maxDate', dateStr)
    },
    updateForm (data) {
      this.form.title = data.title
      this.form.description = data.description
      this.form.startTime = new Date(data.start_time)
      this.form.endTime = new Date(data.end_time)
      this.form.location = data.location
      this.form.public = data.public
      this.form.requireApprove = data.require_approve
    },
    onSubmit (evt) {
      evt.preventDefault()
      const data = {
        title: this.form.title,
        description: this.form.description,
        start_time: new Date(this.form.startTime).toISOString(),
        end_time: new Date(this.form.endTime).toISOString(),
        location: this.form.location,
        public: this.form.public,
        require_approve: this.form.requireApprove
      }
      if (this.newEvent) {
        let eventId
        this.axios.post('/api/event/', data)
          .then(res => {
            eventId = res.data.id
            return this.axios.post('/api/assignadmin/', {
              event_id: eventId
            })
          })
          .then(res => {
            this.$router.push('/event/' + eventId)
          })
      } else {
        this.axios.put('/api/event/' + this.$route.params.id + '/', data)
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
      this.axios.get('/api/event/' + this.$route.params.id)
        .then(res => this.updateForm(res.data))
    }
  }
}
</script>
