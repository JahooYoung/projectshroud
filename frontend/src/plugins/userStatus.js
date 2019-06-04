import { mapState } from 'vuex'
// import { loadLanguageAsync } from '@/plugins/i18n'

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
          this.$root.$bvToast.toast(this.$t('You need to login first'), {
            title: this.$t('Not login yet'),
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
          this.$root.$bvToast.toast(this.$t('You need to activate first'), {
            title: this.$t('Not activated yet'),
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
              this.$root.$bvToast.toast(this.$t('Click here to activate your account!'), {
                title: this.$t('Account not activated'),
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
              this.$root.$bvToast.toast(this.$t('Your signin seems expired, click here to login again!'), {
                title: this.$t('Error'),
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
