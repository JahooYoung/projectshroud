<template>

</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Utils',
  data () {
    return {
      isLoading: false
    }
  },
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
    },
    startLoading () {
      this.isLoading = true
    },
    stopLoading () {
      this.isLoading = false
    }
  }
}
</script>

<style>

</style>
