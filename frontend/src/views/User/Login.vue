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
              id="usernameInputGroup"
              :label="$t('Username:')"
              label-for="usernameInput"
            >
              <b-form-input
                id="usernameInput"
                v-model="form.username"
                autofocus
                type="text"
                required
              />
            </b-form-group>
            <b-form-group
              id="passwordInputGroup"
              :label="$t('Password:')"
              label-for="passwordInput"
            >
              <b-form-input
                id="passwordInput"
                v-model="form.password"
                type="password"
                required
              />
            </b-form-group>
            <b-button
              class="mr-md-3"
              type="submit"
              variant="primary"
            >
              {{ $t('Login') }}
            </b-button>
            <b-button
              to="/register"
              variant="danger"
            >
              {{ $t('Register') }}
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
  // directives: {
  //   focus: {
  //     inserted: el => {
  //       el.focus()
  //     }
  //   }
  // },
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit () {
      this.axios.post('/api/auth/login/', {
        username: this.form.username,
        password: this.form.password
      })
        .then(res => {
          this.$store.commit('setUserState', {
            user: this.form.username,
            key: res.data.key
          })
          return this.checkUserActivation()
        })
        .then(() => {
          if (window.history.length > 1) {
            this.$router.back()
          } else {
            this.$router.push('/')
          }
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
