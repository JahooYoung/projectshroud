<template>
  <b-container>
    <b-row>
      <b-col
        md="8"
        class="mb-3"
      >
        <b-card>
          <h4 class="mb-3">
            {{ $t('Edit Profile') }}
          </h4>
          <b-form @submit.prevent="save">
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              :label="$t('Mobile')"
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
              :label="$t('Real Name')"
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
              :label="$t('Email')"
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
                    {{ $t('Activated') }}
                  </b-button>
                  <b-button
                    v-else
                    variant="warning"
                    :disabled="isLoading"
                    @click="activate"
                  >
                    {{ $t('Activate') }}
                  </b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
            <b-form-group
              label-cols-sm="4"
              label-cols-lg="3"
              :label="$t('Receive Email?')"
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
              {{ $t('Save') }}
            </b-button>
            <b-button
              class="ml-5"
              variant="info"
              to="/change-password"
            >
              {{ $t('Change Password') }}
            </b-button>
          </b-form>
        </b-card>

        <b-modal
          id="modal-activate-email"
          :title="$t('Email Activation')"
          lazy
          @ok="refresh"
        >
          <p v-html="$t('UserProfile.vue confirm email',[userProfile.email])" />
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
            {{ $t('UserProfile.vue fill1',["Registered Events: 10"]) }} <br>
            {{ $t('UserProfile.vue fill2',["Managed Events: 20"]) }}
          </b-card-text>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {
  BCard, BCardText, BForm, BFormGroup, BFormInput, BButton, BInputGroup,
  BInputGroupAppend, BFormCheckbox
} from 'bootstrap-vue'

export default {
  name: 'UserProfile',
  components: {
    BCard,
    BCardText,
    BForm,
    BFormGroup,
    BFormInput,
    BButton,
    BInputGroup,
    BInputGroupAppend,
    BFormCheckbox
  },
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
        this.toastError(this.$t('Please save your profile first'))
        return
      }
      // send confirmation email
      await this.axios.get('/api/send/activation/')
      this.$bvModal.show('modal-activate-email')
    },
    async save () {
      const message = this.$t('Are you sure to change your profile?') +
        this.$t('You\'ll need to reactivate your account if your email is changed.')
      const ans = await this.$bvModal.msgBoxConfirm(message, {
        // centered: true,
        title: this.$t('Confirm'),
        okTitle: this.$t('OK'),
        cancelTitle: this.$t('Cancel')
      })
      if (!ans) {
        return
      }
      try {
        const res = await this.axios.put(`/api/users/${this.userProfile.id}/`, this.userProfile)
        this.savedUserProfile = res.data
        this.toastSuccess(this.$t('Profile saved successfully'))
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
