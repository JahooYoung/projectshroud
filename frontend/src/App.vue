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
import { whiteList } from '@/router'
import NavBar from '@/components/NavBar.vue'
// import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar
    // Footer
  },
  watch: {
    'user': 'checkUserActivation'
  },
  created () {
    this.checkUserActivation()

    this.$router.beforeEach((to, from, next) => {
      if (whiteList.indexOf(to.name) === -1 && !this.checkActivated()) {
        next(false)
        this.$nprogress.setComplete()
      } else {
        next()
      }
    })

    this.axios.interceptors.response.use(res => res, err => {
      if (!err.response) {
        this.$bvToast.toast('Fail to connect server', {
          title: 'Network Error',
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
            // call `checkLogin()`, so I call it here.
            this.checkLogin()
            break
          case 403:
            // Forbidden: user does not have permission.
            this.$bvToast.toast('You do not have permission', {
              title: 'Forbidden',
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
            this.$bvToast.toast('It seems some error occured in the server', {
              title: 'Internal Server Error',
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
          default:
            this.$bvToast.toast('Unknown status code ' + err.response.status, {
              title: 'Unknown Error',
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
  },
  methods: {
    checkUserActivation () {
      if (!this.user) {
        return
      }
      this.axios.get('/api/dummy/')
        .then(res => {
          this.$store.commit('setUserActivation', res.data.is_activated)
          if (!res.data.is_activated) {
            this.$bvToast.toast('Click here to activate your account!', {
              title: 'Account not activated',
              variant: 'warning',
              autoHideDelay: 5000,
              solid: true,
              to: '/user-profile'
            })
          }
        })
        .catch(() => {
          this.$store.commit('setUserState', null)
          this.$bvToast.toast('Your signin seems expired, click here to login again!', {
            title: 'Error',
            variant: 'danger',
            autoHideDelay: 5000,
            solid: true,
            to: '/login'
          })
        })
    }
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
