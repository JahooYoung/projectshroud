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
            <!-- <p v-html="$t('test html-format')"></p> -->
            <b-form-group
              id="mobileInputGroup"
              :label="$t('Mobile:')"
              label-for="mobileInput"
              label-cols-sm="4"
              label-cols-lg="3"
              :state="($v.mobile.$dirty || null) && !$v.mobile.$error"
              :valid-feedback="$t('This mobile is available!')"
            >
              <b-form-input
                id="mobileInput"
                v-model.trim="$v.mobile.$model"
                autofocus
                @blur="$v.mobile.$touch()"
              />
              <template #invalid-feedback>
                <div v-if="!$v.mobile.required">
                  {{ $t('This field is required.') }}
                </div>
                <div v-else-if="!$v.mobile.minLength || !$v.mobile.maxLength">
                  {{ $t('Must have exactly digits.',[$v.mobile.$params.minLength.min]) }}
                </div>
                <div v-else-if="!$v.mobile.numeric">
                  {{ $t('Must be numeric.') }}
                </div>
                <div v-else-if="!$v.mobile.noServerError">
                  {{ $t('Register.vue username',[err.username[0]]) }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="emailInputGroup"
              :label="$t('Email:')"
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
                  {{ $t('This field is required.') }}
                </div>
                <div v-if="!$v.email.email">
                  {{ $t('Please input a valid email') }}
                </div>
                <div v-else-if="!$v.email.noServerError">
                  {{ $t('Register.vue email', [err.email[0]]) }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="passwordInputGroup"
              :label="$t('Password:')"
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
                  {{ $t('This field is required.') }}
                </div>
                <div v-else-if="!$v.password.minLength">
                  {{ $t('Password must contain at least characters',[$v.password.$params.minLength.min]) }}
                </div>
                <div v-else-if="!$v.password.complex">
                  {{ $t('Password can not contains only digits, only lowercase alpha or only uppercase alpha.') }}
                </div>
                <div v-else-if="!$v.password.uncommon">
                  {{ $t('This password is too common.') }}
                </div>
                <div v-else-if="!$v.password.noServerError">
                  {{ $t('Register.vue password', err.password1[0]) }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="RepeatPasswordInputGroup"
              :label="$t('Repeat password:')"
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
                  {{ $t('Two passwords are different!') }}
                </div>
              </template>
            </b-form-group>

            <b-form-group
              id="realNameInputGroup"
              :label="$t('Real name:')"
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
                  {{ $t('This field is required.') }}
                </div>
                <div v-else-if="!$v.realName.noServerError">
                  {{ err.realName[0] }}
                </div>
              </template>
            </b-form-group>

            <b-button
              type="submit"
              variant="primary"
              :disabled="$v.$invalid"
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
import { validationMixin } from 'vuelidate'
import { required, minLength, maxLength, numeric, sameAs, email, helpers, not } from 'vuelidate/lib/validators'

export default {
  name: 'Register',
  components: {
    BForm,
    BFormGroup,
    BFormInput,
    BButton
  },
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
        return value !== this.submitted.realName || !this.err.realName
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
          realName: this.realName
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
