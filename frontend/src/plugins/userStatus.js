import { mapState } from 'vuex'

function UserStatus() {}

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
          this.$bvToast.toast('You need to login first', {
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
          this.$bvToast.toast('You need to activate first', {
            title: 'Not activated yet',
            variant: 'warning',
            autoHideDelay: 4000,
            solid: true,
            to: '/user-profile'
          })
          return false
        }
        return true
      }
    }
  })
}

export default UserStatus
