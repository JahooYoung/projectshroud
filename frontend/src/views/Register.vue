<template>
  <div>
    <b-form @submit="onSubmit">

      <b-container>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-form-group
              id="usernameInputGroup"
              label="Username:"
              label-for="usernameInput"
              >
              <b-form-input
                id="usernameInput"
                type="text"
                v-model="form.username"
                required/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-form-group
              id="passwordInputGroup"
              label="Password:"
              label-for="passwordInput"
              >
              <b-form-input
                id="passwordInput"
                type="password"
                v-model="form.password"
                required/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-form-group
              id="RepeatPasswordInputGroup"
              label="Repeat password:"
              label-for="repeatPasswordInput"
              >
              <b-form-input
                id="repeatPasswordInput"
                type="password"
                v-model="form.repeatPassword"
                required/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-form-group
              id="emailInputGroup"
              label="Email:"
              label-for="emailInput"
              >
              <b-form-input
                id="emailInput"
                type="email"
                v-model="form.email"
                required/>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-button type="submit" variant="primary">Register</b-button>
          </b-col>
        </b-row>
      </b-container>

    </b-form>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      form: {
        username: '',
        password: '',
        repeatPassword: '',
        email: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.axios.post('api/auth/registration/', {
        username: this.form.username,
        password1: this.form.password,
        password2: this.form.repeatPassword,
        email: this.form.email,
        real_name: 'Hello'
      })
        .then(res => {
          if (res.status === 201) {
            this.$store.commit('setUserState', {
              user: this.form.username,
              key: res.data.key
            })
            this.$router.back()
          } else {
            alert(JSON.stringify(res.data))
          }
        })
        .catch(err => {
          console.log(err)
          alert('register failed')
        })
    }
  }
}
</script>
