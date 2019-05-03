<template>
  <div>
    <b-form @submit="onSubmit">
      <b-container fluid>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              id="mobileInputGroup"
              label="Mobile:"
              label-for="mobileInput"
              label-cols-sm="4"
              label-cols-lg="3"
            >
              <b-form-input
                id="mobileInput"
                v-model="form.mobile"
                type="text"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              id="passwordInputGroup"
              label="Password:"
              label-for="passwordInput"
              label-cols-sm="4"
              label-cols-lg="3"
            >
              <b-form-input
                id="passwordInput"
                v-model="form.password"
                type="password"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              id="RepeatPasswordInputGroup"
              label="Repeat password:"
              label-for="repeatPasswordInput"
              label-cols-sm="4"
              label-cols-lg="3"
            >
              <b-form-input
                id="repeatPasswordInput"
                v-model="form.repeatPassword"
                type="password"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              id="realNameInputGroup"
              label="Real name:"
              label-for="realNameInput"
              label-cols-sm="4"
              label-cols-lg="3"
            >
              <b-form-input
                id="realNameInput"
                v-model="form.realName"
                type="realName"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-form-group
              id="emailInputGroup"
              label="Email:"
              label-for="emailInput"
              label-cols-sm="4"
              label-cols-lg="3"
            >
              <b-form-input
                id="emailInput"
                v-model="form.email"
                type="email"
                required
              />
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col
            cols="12"
            offset-md="3"
            md="6"
            offset-lg="4"
            lg="4"
          >
            <b-button
              type="submit"
              variant="primary"
            >
              Register
            </b-button>
          </b-col>
        </b-row>
      </b-container>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      form: {
        mobile: '',
        password: '',
        repeatPassword: '',
        email: '',
        realName: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.axios.post('/api/auth/registration/', {
        username: this.form.mobile,
        password1: this.form.password,
        password2: this.form.repeatPassword,
        email: this.form.email,
        real_name: this.form.realName
      })
        .then(res => {
          this.$store.commit('setUserState', {
            user: this.form.mobile,
            key: res.data.key
          })
          this.$router.back()
        })
        .catch(err => err.response && alert(JSON.stringify(err.response.data)))
    }
  }
}
</script>
