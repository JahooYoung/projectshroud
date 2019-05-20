import { mapState } from 'vuex'

function UserStatus () {}

UserStatus.install = function (Vue, options = {}) {
  if (this.installed) {
    return
  }
  this.installed = true

  Vue.mixin({
    computed: mapState(['user', 'userActivated']),
    methods: {
      checkLogin () {
        if (!this.user) {
          this.$root.$bvToast.toast('You need to login first', {
            title: 'Not login yet',
            variant: 'warning',
            autoHideDelay: 4000,
            solid: true,
            to: '/login'
          })
          return false
        }
        return true
      },
      checkActivated () {
        if (!this.checkLogin()) {
          return false
        }
        if (!this.userActivated) {
          this.$root.$bvToast.toast('You need to activate first', {
            title: 'Not activated yet',
            variant: 'warning',
            autoHideDelay: 4000,
            solid: true,
            to: '/user-profile'
          })
          return false
        }
        return true
      },
      checkUserActivation () {
        return this.axios.get('/api/dummy/')
          .then(res => {
            this.$store.commit('setUserActivation', res.data.isActivated)
            if (!res.data.isActivated) {
              this.$root.$bvToast.toast('Click here to activate your account!', {
                title: 'Account not activated',
                variant: 'warning',
                autoHideDelay: 5000,
                solid: true,
                to: '/user-profile'
              })
            }
          })
          .catch(err => {
            if (err.response && err.response.status >= 400 && err.response.status < 500) {
              this.$store.commit('setUserState', null)
              this.$root.$bvToast.toast('Your signin seems expired, click here to login again!', {
                title: 'Error',
                variant: 'danger',
                autoHideDelay: 5000,
                solid: true,
                to: '/login'
              })
            }
          })
      }
    }
  })
}

export default UserStatus
