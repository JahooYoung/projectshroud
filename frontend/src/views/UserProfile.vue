<template>
  <b-container>
    <b-row>
      <b-col
        md="8"
        class="mb-3"
      >
        <b-card>
          <h4 class="mb-3">
            Edit Profile
          </h4>
          <b-form @submit.prevent="saveUserProfile">
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              label="Mobile"
              label-for="mobileInput"
            >
              <b-form-input
                id="mobileInput"
                v-model="mobile"
                required
              />
            </b-form-group>
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              label="Real Name"
              label-for="realNameInput"
            >
              <b-form-input
                id="realNameInput"
                v-model="realName"
                required
              />
            </b-form-group>
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              label="Email"
              label-for="emailInput"
            >
              <b-input-group>
                <b-form-input
                  id="emailInput"
                  v-model="email"
                  required
                />
                <b-input-group-append>
                  <b-button
                    v-if="userActivated"
                    variant="success"
                    disabled
                  >
                    activated
                  </b-button>
                  <b-button
                    v-else
                    variant="warning"
                    :disabled="isLoading"
                    @click="activate"
                  >
                    activate
                  </b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>

            <b-button
              variant="primary"
              type="submit"
              :disabled="!modified || isLoading"
            >
              <b-spinner
                v-show="isLoading"
                small
                type="grow"
              />
              Save
            </b-button>
          </b-form>
        </b-card>

        <b-modal
          id="modal-activate-email"
          title="Email Activation"
          lazy
          @ok="refresh"
        >
          A confirmation email was sent to <b>{{ email }}</b>. <br>
          Click "ok" after the confirmation succeeds.
        </b-modal>
      </b-col>
      <b-col md="4">
        <b-card
          :title="realName"
          img-src="https://placekitten.com/g/400/200"
          img-alt="Image"
          img-top
        >
          <b-card-text>
            Registered Events: 10 <br>
            Managed Events: 20
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'UserProfile',
  data () {
    return {
      userProfile: null,
      mobile: '',
      realName: '',
      email: ''
    }
  },
  computed: {
    modified () {
      return this.userProfile && (this.mobile !== this.userProfile.mobile ||
        this.realName !== this.userProfile.real_name ||
        this.email !== this.userProfile.email)
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/user/')
        .then(res => {
          this.userProfile = res.data
          this.mobile = res.data.mobile
          this.realName = res.data.real_name
          this.email = res.data.email
          this.$store.commit('setUserActivation', res.data.is_activated)
        })
    },
    activate () {
      // check saved?
      if (this.modified) {
        this.$bvToast.toast('Please save your profile first', {
          title: 'Error',
          variant: 'danger',
          autoHideDelay: 5000,
          solid: true
        })
        return
      }
      // send confirmation email
      this.axios.get('/api/send/activation/')
        .then(res => {
          this.$bvModal.show('modal-activate-email')
        })
    },
    saveUserProfile () {
      this.axios.put(`/api/users/${this.userProfile.id}/`, {
        mobile: this.mobile,
        real_name: this.realName,
        email: this.email
      })
        .then(res => {
          this.$bvToast.toast('Profile saved successfully', {
            title: 'Success',
            autoHideDelay: 3000,
            solid: true
          })
          this.refresh()
        })
        .catch(err => {
          if (err.response) {
            alert(JSON.stringify(err.response.data))
          }
        })
    }
  }
}
</script>

<style>

</style>
