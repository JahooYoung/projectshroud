<template>
  <div>
    <b-form @submit.prevent="onSubmit">
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
              :state="($v.mobile.$dirty || null) && !$v.mobile.$error"
              :valid-feedback="`${$v.mobile.$model} is available!`"
            >
              <b-form-input
                id="mobileInput"
                v-model.trim="$v.mobile.$model"
                @blur="$v.mobile.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.mobile.required">
                  This field is required.
                </div>
                <div v-else-if="!$v.mobile.minLength || !$v.mobile.maxLength">
                  Must have exactly {{ $v.mobile.$params.minLength.min }} digits.
                </div>
                <div v-else-if="!$v.mobile.numeric">
                  Must be numeric.
                </div>
                <div v-else-if="!$v.mobile.noServerError">
                  {{ err.username[0] }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="emailInputGroup"
              label="Email:"
              label-for="emailInput"
              label-cols-sm="4"
              label-cols-lg="3"
              :state="!$v.email.$error"
            >
              <b-form-input
                id="emailInput"
                v-model.trim="$v.email.$model"
                @blur="$v.email.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.email.required">
                  This field is required.
                </div>
                <div v-if="!$v.email.email">
                  Please input a valid email
                </div>
                <div v-else-if="!$v.email.noServerError">
                  {{ err.email[0] }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="passwordInputGroup"
              label="Password:"
              label-for="passwordInput"
              label-cols-sm="4"
              label-cols-lg="3"
              :state="!$v.password.$error"
            >
              <b-form-input
                id="passwordInput"
                v-model.trim="$v.password.$model"
                type="password"
                @blur="$v.password.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.password.required">
                  This field is required.
                </div>
                <div v-else-if="!$v.password.minLength">
                  At least {{ $v.password.$params.minLength.min }} characters.
                </div>
                <div v-else-if="!$v.password.complex">
                  Password can not contains only digits, only lowercase alpha or only uppercase alpha.
                </div>
                <div v-else-if="!$v.password.uncommon">
                  This password is too common.
                </div>
                <div v-else-if="!$v.password.noServerError">
                  {{ err.password1[0] }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="RepeatPasswordInputGroup"
              label="Repeat password:"
              label-for="repeatPasswordInput"
              label-cols-sm="4"
              label-cols-lg="3"
              :state="!$v.repeatPassword.$error"
            >
              <b-form-input
                id="repeatPasswordInput"
                v-model.trim="$v.repeatPassword.$model"
                type="password"
                @blur="$v.repeatPassword.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.repeatPassword.sameAsPassword">
                  Two passwords are different!
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="realNameInputGroup"
              label="Real name:"
              label-for="realNameInput"
              label-cols-sm="4"
              label-cols-lg="3"
              :state="!$v.realName.$error"
            >
              <b-form-input
                id="realNameInput"
                v-model.trim="$v.realName.$model"
                @blur="$v.realName.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.realName.required">
                  This field is required.
                </div>
                <div v-else-if="!$v.realName.noServerError">
                  {{ err.real_name[0] }}
                </div>
              </template>
            </b-form-group>

            <b-button
              type="submit"
              variant="primary"
              :disabled="$v.$invalid"
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
import { validationMixin } from 'vuelidate'
import { required, minLength, maxLength, numeric, sameAs, email, helpers, not } from 'vuelidate/lib/validators'

export default {
  name: 'Register',
  mixins: [validationMixin],
  data () {
    return {
      mobile: '',
      password: '',
      repeatPassword: '',
      email: '',
      realName: '',
      submitted: {},
      err: {},
      commonPasswords: null
    }
  },
  created () {
    this.axios.get('/common-passwords.new.txt')
      .then(res => {
        this.commonPasswords = res.data.split('\n')
      })
      .catch(() => {
        this.commonPasswords = []
      })
  },
  validations: {
    mobile: {
      required,
      minLength: minLength(11),
      maxLength: maxLength(11),
      numeric,
      noServerError (value) {
        return value !== this.submitted.username || !this.err.username
      }
    },
    password: {
      required,
      minLength: minLength(8),
      complex: not(helpers.regex('complex', /^([\d]*|[a-z]*|[A-Z]*)$/)),
      uncommon (value) {
        return this.commonPasswords && this.commonPasswords.indexOf(value.toLowerCase()) === -1
      },
      noServerError (value) {
        return value !== this.submitted.password1 || !this.err.password1
      }
    },
    repeatPassword: {
      sameAsPassword: sameAs('password')
    },
    email: {
      required,
      email,
      noServerError (value) {
        return value !== this.submitted.email || !this.err.email
      }
    },
    realName: {
      required,
      noServerError (value) {
        return value !== this.submitted.real_name || !this.err.real_name
      }
    }
  },
  methods: {
    async onSubmit () {
      try {
        this.err = {}
        this.submitted = {
          username: this.mobile,
          password1: this.password,
          password2: this.repeatPassword,
          email: this.email,
          real_name: this.realName
        }
        const res = await this.axios.post('/api/auth/registration/', this.submitted)
        this.$store.commit('setUserState', {
          user: this.mobile,
          key: res.data.key
        })
        await this.checkUserActivation()
        if (window.history.length > 2) {
          this.$router.go(-2)
        } else {
          this.$router.push('/')
        }
      } catch (err) {
        if (err.response && err.response.status === 400) {
          this.err = err.response.data
          this.$v.$touch()
        }
      }
    }
  }
}
</script>
