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
          <b-form @submit.prevent="save">
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              label="Mobile"
              label-for="mobileInput"
            >
              <b-form-input
                id="mobileInput"
                v-model="userProfile.mobile"
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
                v-model="userProfile.realName"
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
                  v-model="userProfile.email"
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
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              label="Receive Email"
            >
              <div style="text-align: left;">
                <b-form-checkbox
                  v-model="userProfile.receiveEmail"
                  size="lg"
                  switch
                />
              </div>
            </b-form-group>

            <b-button
              variant="primary"
              type="submit"
              :disabled="!modified || isLoading"
            >
              Save
            </b-button>
            <b-button
              class="ml-5"
              variant="info"
              to="/change-password"
            >
              Change Password
            </b-button>
          </b-form>
        </b-card>

        <b-modal
          id="modal-activate-email"
          title="Email Activation"
          lazy
          @ok="refresh"
        >
          A confirmation email was sent to <b>{{ userProfile.email }}</b>. <br>
          Click "ok" after the confirmation succeeds.
        </b-modal>
      </b-col>
      <b-col md="4">
        <b-card
          :title="userProfile.realName"
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
      savedUserProfile: null,
      userProfile: {
        mobile: '',
        realName: '',
        email: '',
        receiveEmail: true
      }
    }
  },
  computed: {
    modified () {
      if (!this.savedUserProfile) {
        return false
      }
      for (let key in this.userProfile) {
        if (this.userProfile[key] !== this.savedUserProfile[key]) {
          return true
        }
      }
      return false
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    async refresh () {
      const res = await this.axios.get('/api/user/')
      this.savedUserProfile = res.data
      this.userProfile = Object.assign({}, res.data)
      this.$store.commit('setUserActivation', res.data.isActivated)
    },
    async activate () {
      // check saved?
      if (this.modified) {
        this.toastError('Please save your profile first')
        return
      }
      // send confirmation email
      await this.axios.get('/api/send/activation/')
      this.$bvModal.show('modal-activate-email')
    },
    async save () {
      try {
        const res = await this.axios.put(`/api/users/${this.userProfile.id}/`, this.userProfile)
        this.savedUserProfile = res.data
        this.toastSuccess('Profile saved successfully')
        this.refresh()
      } catch (err) {
        if (err.needHandle) {
          alert(JSON.stringify(err.response.data))
        }
      }
    }
  }
}
</script>
