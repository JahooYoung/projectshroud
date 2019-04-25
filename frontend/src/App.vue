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
// import Utils from '@/components/Utils.vue'
import NavBar from '@/components/NavBar.vue'
// import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  // mixins: [Utils],
  components: {
    NavBar
    // Footer
  },
  created () {
    this.checkUserActivation()

    this.$router.beforeEach((to, from, next) => {
      if (whiteList.indexOf(to.name) === -1) {
        if (!this.checkActivated()) {
          next(false)
          this.$nprogress.setComplete()
        } else {
          next()
        }
      } else {
        if (this.user && (to.name === 'login' || to.name === 'register')) {
          next('/')
        } else {
          next()
        }
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
        if (err.response.data.detail) {
          this.$bvToast.toast(err.response.data.detail, {
            title: 'Error',
            variant: 'secondary',
            autoHideDelay: 4000,
            solid: true
          })
        }
      }
      return Promise.reject(err)
    })
  },
  watch: {
    'user': 'checkUserActivation'
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
              autoHideDelay: 10000,
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
            autoHideDelay: 10000,
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
