<template>
  <div>
    <b-form @submit.prevent="onSubmit">
      <b-container>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              :label="$t('Old Password:')"
              label-for="oldPasswordInput"
            >
              <b-form-input
                id="oldPasswordInput"
                v-model="form.oldPassword"
                type="password"
                autofocus
                required
              />
            </b-form-group>
            <b-form-group
              :label="$t('New Password:')"
              label-for="newPasswordInput"
            >
              <b-form-input
                id="newPasswordInput"
                v-model="form.newPassword"
                type="password"
                required
              />
            </b-form-group>
            <b-form-group
              :label="$t('Repeat New Password:')"
              label-for="repeatNewPasswordInput"
            >
              <b-form-input
                id="repeatNewPasswordInput"
                v-model="form.repeatNewPassword"
                type="password"
                required
              />
            </b-form-group>
            <b-button
              class="mr-md-3"
              type="submit"
              variant="primary"
            >
              {{ $t('Confirm') }}
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'ChangePassword',
  data () {
    return {
      form: {
        oldPassword: '',
        newPassword: '',
        repeatNewPassword: ''
      }
    }
  },
  methods: {
    async onSubmit () {
      try {
        await this.axios.post('/api/auth/password/change/', {
          oldPassword: this.form.oldPassword,
          newPassword1: this.form.newPassword,
          newPassword2: this.form.repeatNewPassword
        })
        this.toastSuccess(this.$t('Successfully change password!'))
        this.$router.back()
      } catch (err) {
        if (err.needHandle) {
          alert(JSON.stringify(err.response.data))
        }
      }
    }
  }
}
</script>
