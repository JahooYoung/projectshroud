<template>
  <div id="app">
    <div class="nprogress-container" />
    <NavBar />
    <transition
      name="fade"
      mode="out-in"
    >
      <router-view />
    </transition>
    <!-- <Footer/> -->
  </div>
</template>

<script>
// @ is an alias to /src
import { whiteList } from '@/plugins/router'
import NavBar from '@/components/NavBar.vue'
// import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar
    // Footer
  },
  created () {
    if (this.user) {
      this.checkUserActivation()
    }

    this.$router.beforeEach((to, from, next) => {
      if (whiteList.indexOf(to.name) === -1 && !this.checkActivated()) {
        next(false)
        this.$nprogress.setComplete()
      } else {
        next()
      }
    })

    this.axios.interceptors.response.use(res => res, err => {
      err.needHandle = true
      if (!err.response) {
        err.needHandle = false
        this.$bvToast.toast(this.$t('Fail to connect server'), {
          title: this.$t('Network Error'),
          variant: 'secondary',
          autoHideDelay: 4000,
          solid: true
        })
      } else {
        //! this should be the only `console.log` of network request
        console.log(err.response)
        switch (err.response.status) {
          case 400:
            // Bad Request: most of these are validation error.
            // Should be processed by the caller.
            break
          case 401:
            // Unauthorized: probably not login.
            // If 401 is returned, it is probable that you forget to
            // call `checkLogin()`.
            // this.checkLogin()
            break
          case 403:
            // Forbidden: user does not have permission.
            err.needHandle = false
            this.$bvToast.toast(this.$t('You do not have permission'), {
              title: this.$t('Forbidden'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
          case 404:
            // Not Found: the resource is not existed.
            // Should be processed by the caller.
            break
          case 500:
            // Internal Server Error
            err.needHandle = false
            this.$bvToast.toast(this.$t('It seems some error occured in the server'), {
              title: this.$t('Internal Server Error'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
          default:
            err.needHandle = false
            this.$bvToast.toast(this.$t('Unknown status code ') + err.response.status, {
              title: this.$t('Unknown Error'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
        }
      }
      return Promise.reject(err)
    })

    document.querySelector('#first-page-spinner').remove()
  }
}
</script>

<style>
@import '~nprogress/nprogress.css';

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .15s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
