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
          <b-form-input
            v-model="form.startTime"
            id="startTimeInput"
            type="datetime-local"
            required
          />
        </b-form-group>
        <b-form-group
          id="endTimeInputGroup"
          label-cols-sm="4"
          label-cols-lg="3"
          label="End time"
          label-for="endTimeInput"
        >
          <b-form-input
            v-model="form.endTime"
            id="endTimeInput"
            type="datetime-local"
            required
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
function date2input (date) {
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  date.setSeconds(0, 0)
  date = date.toISOString()
  return date.substr(0, date.length - 1)
}

function input2date (str) {
  let date = new Date(str)
  return date
}

export default {
  name: 'Info',
  props: {
    newEvent: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoading: false,
      buttonName: 'Save',
      form: {
        title: '',
        description: '',
        startTime: '',
        endTime: '',
        location: '',
        public: false,
        requireApprove: false
      }
    }
  },
  mounted () {
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
    onSubmit (e) {
      e.preventDefault()
      const data = {
        title: this.form.title,
        description: this.form.description,
        start_time: input2date(this.form.startTime).toISOString(),
        end_time: input2date(this.form.endTime).toISOString(),
        location: this.form.location,
        public: this.form.public,
        require_approve: this.form.requireApprove
      }
      if (this.newEvent) {
        this.isLoading = true
        this.axios.post('/api/event/', data)
          .then(res => {
            this.isLoading = false
            if (res.status === 201) {
              // this.$bvToast.toast(`Event "${res.data.title}" created successfully`, {
              //   title: `Success`,
              //   autoHideDelay: 5000,
              //   solid: true
              // })
              const eventId = res.data.id
              this.isLoading = true
              this.axios.post('/api/assignadmin/', {
                event_id: eventId
              })
                .then(res => {
                  this.isLoading = false
                  if (res.status === 201) {
                    this.$router.push('/event/' + eventId)
                  } else {
                    alert(JSON.stringify(res.data))
                  }
                })
                .catch(err => {
                  this.isLoading = false
                  console.log('failed to assign admin', err)
                })
            } else {
              alert(JSON.stringify(res.data))
            }
          })
          .catch(err => {
            this.isLoading = false
            console.log('failed to create events\n', err)
          })
      } else {
        this.isLoading = true
        this.axios.put('/api/event/' + this.$route.params.id + '/', data)
          .then(res => {
            if (res.status === 200) {
              this.$bvToast.toast(`Event "${res.data.title}" saved successfully`, {
                title: `Success`,
                autoHideDelay: 5000,
                solid: true
              })
              this.refresh()
            }
          })
          .catch(err => {
            this.isLoading = false
            console.log('failed to update events\n', err)
          })
      }
    },
    refresh () {
      this.isLoading = true
      this.axios.get('/api/event/' + this.$route.params.id)
        .then(res => {
          this.isLoading = false
          console.log(res.data)
          this.form.title = res.data.title
          this.form.description = res.data.description
          this.form.startTime = date2input(new Date(res.data.start_time))
          this.form.endTime = date2input(new Date(res.data.end_time))
          this.form.location = res.data.location
          this.form.public = res.data.public
          this.form.requireApprove = res.data.require_approve
        })
        .catch(err => {
          this.isLoading = false
          console.log('failed to fetch events\n', err)
        })
    }
  }
}
</script>
