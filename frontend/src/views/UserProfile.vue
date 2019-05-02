<template>
  <b-container>
    <b-row>
      <b-col md="8">
        <b-card>
          <h4 class="mb-3">Edit Profile</h4>
          <b-form @submit="saveUserProfile">
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
              :disabled="isLoading"
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
          @ok="refreshUserState"
        >
          A confirmation email was sent to <b>{{ email }}</b>. <br>
          Click "ok" after the confirmation succeeds.
        </b-modal>
      </b-col>
      <b-col cols="4">
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
      mobile: '',
      realName: '',
      email: ''
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.mobile = this.user
      this.realName = 'Rio Nem'
      this.email = 'admin@testshroud.top'
    },
    activate () {
      // check saved?
      // send confirmation email
      this.$bvModal.show('modal-activate-email')
    },
    saveUserProfile () {

    },
    refreshUserState () {

    }
  }
}
</script>

<style>

</style>
