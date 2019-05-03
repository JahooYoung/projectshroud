<template>
  <div>
    <b-form @submit="onSubmit">
      <b-container fluid>
        <b-row>
          <b-col cols="12" offset-md="2" md="6" offset-lg="4" lg="4">
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
                :state="mobileCheck"
                placeholder="Enter a number"
                required/>
              <b-form-invalid-feedback id="mobileInput">
                <!--Enter a number-->
              </b-form-invalid-feedback>
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
                type="password"
                v-model="form.password"
                :state="passwordCheck"
                required/>
              <b-form-invalid-feedback id="passwordInput">
                Password can only contain 0-9, a-z and underlines, and must have length 6-16
              </b-form-invalid-feedback>
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
                type="password"
                v-model="form.repeatPassword"
                :state="repeatPasswordCheck"
                required/>
              <b-form-invalid-feedback id="repeatPasswordInput">
                Password and repeat password must be the same
              </b-form-invalid-feedback>
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
                :state="emailCheck"
                placeholder="example@example.com"
                required/>
              <b-form-invalid-feedback id="emailInput">
                invalid email
              </b-form-invalid-feedback>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="12" offset-md="3" md="6" offset-lg="4" lg="4">
            <b-button variant="primary" type="submit" :disabled="!allCheck">
              Register
            </b-button>
          </b-col>
        </b-row>
      </b-container>
      <b-modal ref="modal-registerAccount" @ok="mailConfirm" title="Register Account">
        <p class="my-4">We've sent you an email. Please click on the link in it to confirm your register.</p>
      </b-modal>

    </b-form>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      form: {
        mobile: '11111111',
        password: '111111aaaa',
        repeatPassword: '111111aaaa',
        email: 'example@example.com',
        realName: '123'
      }
    }
  },
  computed: {
    mobileCheck() {
      if(!(/^[0-9]+$/.test(this.form.mobile)))
        return false;
      return true;
    },
    passwordCheck() {
      return this.form.password.length>=6 && this.form.password.length<=16 && /^\w+$/.test(this.form.password);
    },
    repeatPasswordCheck() {
      return this.form.repeatPassword === this.form.password;
    },
    emailCheck() {
      return /^\w+@\w+(.\w+)+$/.test(this.form.email);
    },
    allCheck() {
      console.log('allCheck')
      return this.mobileCheck && this.passwordCheck
            && this.repeatPasswordCheck && this.emailCheck
    }
  },
  methods: {
    mounted (evt) {

    },
    mailConfirm (evt) {
      console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
      alert('Email have been sent')
      // this.$refs["modal-registerAccount"].show()
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.axios.post('api/auth/registration/', {
        username: this.form.mobile,
        password1: this.form.password,
        password2: this.form.repeatPassword,
        email: this.form.email,
        real_name: this.form.realName
      })
        .then(res => {
          // this.$refs["modal-registerAccount"].show()
          if (res.status === 201) {
            this.$store.commit('setUserState', {
              user: this.form.mobile,
              key: res.data.key
            })
            this.mailConfirm(evt);
            this.$router.go(-1)
            evt.preventDefault()
          } else {
            console.log(res.data);
            alert(JSON.stringify(res.data))
            evt.preventDefault()
          }
        })
        .catch(err => {
          console.log(err)
          alert(JSON.stringify(err))
          alert('register failed')
          evt.preventDefault()
        })
        .catch(err => {
          alert("aaaa")
          err.response && alert(JSON.stringify(err.response.data))
        })
    }
  }
}
</script>
