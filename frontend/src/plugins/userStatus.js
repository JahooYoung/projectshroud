import { mapState } from 'vuex'

function UserStatus () {}

UserStatus.install = function (Vue) {
  if (this.installed) {
    return
  }
  this.installed = true

  Vue.mixin({
    computed: mapState(['user', 'userActivated']),
    methods: {
      checkLogin () {
        if (!this.user) {
          this.toastWarning('You need to login first', null, '/login')
          return false
        }
        return true
      },
      checkActivated () {
        if (!this.checkLogin()) {
          return false
        }
        if (!this.userActivated) {
          this.toastWarning('You need to activate first', null, '/user-profile')
          return false
        }
        return true
      },
      async checkUserActivation () {
        try {
          const res = this.axios.get('/api/dummy/')
          this.$store.commit('setUserActivation', res.data.isActivated)
          if (!res.data.isActivated) {
            this.toastWarning('Click here to activate your account!', 'Account not activated', '/user-profile')
          }
        } catch (err) {
          if (err.response && err.response.status >= 400 && err.response.status < 500) {
            this.$store.commit('setUserState', null)
            this.toastError('Your signin seems expired, click here to login again!', null, '/login')
          }
        }
      }
    }
  })
}

export default UserStatus
