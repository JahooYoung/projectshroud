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
            <b-button type="submit" variant="primary">Login</b-button>
            <b-button to="/register" variant="danger">Register</b-button>
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
        username: 'jahoo',
        password: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.axios.post('api/auth/login/', {
        username: this.form.username,
        password: this.form.password
      })
        .then(res => {
          console.log('login succeed\n', res)
          this.$store.commit('setUserState', {
            user: this.form.username,
            key: res.data.key
          })
          this.$router.back()
        })
        .catch(err => {
          alert('username or password is not correct')
        })
    }
  }
}
</script>
