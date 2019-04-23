<template>
  <div id="app">
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
import NavBar from '@/components/NavBar.vue'
// import Footer from '@/components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar
    // Footer
  },
  created () {
    this.axios.interceptors.response.use(x => x, err => {
      if (err.message === 'Network Error') {
        this.$bvToast.toast('Fail to connect server', {
          title: 'Network Error',
          variant: 'secondary',
          autoHideDelay: 4000,
          solid: true
        })
      }
      //! this should be the only `console.log` of network request
      console.log(err.response)
      return Promise.reject(err)
    })
  }
}
</script>

<style>
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
