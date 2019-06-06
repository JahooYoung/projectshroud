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
              :label="$t('Mobile:')"
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
              :state="!haveErr"
            >
              <b-form-input
                id="passwordInput"
                v-model="form.password"
                type="password"
                required
              />
              <template #invalid-feedback>
                <div v-if="haveErr">
                  {{ $t('Mobile or password is wrong') }}!
                </div>
              </template>
            </b-form-group>
            <b-button
              class="mr-md-3"
              type="submit"
              variant="primary"
              :disabled="haveErr"
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
import { BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue'

export default {
  name: 'Login',
  components: {
    BForm,
    BFormGroup,
    BFormInput,
    BButton
  },
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      haveErr: false
    }
  },
  watch: {
    'form.username' () {
      this.haveErr = false
    },
    'form.password' () {
      this.haveErr = false
    }
  },
  methods: {
    async onSubmit () {
      try {
        const res = await this.axios.post('/api/auth/login/', {
          username: this.form.username,
          password: this.form.password
        })
        this.$store.commit('setUserState', {
          user: this.form.username,
          key: res.data.key
        })
        await this.checkUserActivation()
        if (window.history.length > 1) {
          this.$router.back()
        } else {
          this.$router.push('/')
        }
      } catch (err) {
        if (err.needHandle) {
          this.haveErr = true
        }
      }
    }
  }
}
</script>
