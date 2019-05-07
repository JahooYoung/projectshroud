import Vue from 'vue'
import nprogress from 'nprogress'
import axios from './axios'

const defaults = {
  latencyThreshold: 100,
  router: true,
  http: true
}

function install (Vue, options = {}) {
  if (this.installed) {
    return
  }
  this.installed = true

  Object.defineProperty(Vue.prototype, '$nprogress', {
    get: function get () {
      return this.$root._nprogress
    }
  })

  options = Object.assign({}, defaults, options)

  Vue.mixin({
    computed: {
      isLoading () {
        return this.$store.state.isLoading
      }
    },
    beforeCreate () {
      const np = this.$options.nprogress

      if (!np) {
        return
      }

      let requestsTotal = 0
      let requestsCompleted = 0
      let { latencyThreshold, router: applyOnRouter, http: applyOnHttp } = options
      let confirmed = true

      const store = this.$options.store

      function setComplete () {
        requestsTotal = 0
        requestsCompleted = 0
        np.done()
        store.commit('setLoading', false)
      }

      function initProgress () {
        if (requestsTotal === 0) {
          setTimeout(() => np.start(), latencyThreshold)
          store.commit('setLoading', true)
        }
        requestsTotal++
        np.set(requestsCompleted / requestsTotal)
      }

      function increase () {
        // Finish progress bar 50 ms later
        setTimeout(() => {
          ++requestsCompleted
          if (requestsCompleted >= requestsTotal) {
            setComplete()
          } else {
            np.set((requestsCompleted / requestsTotal) - 0.1)
          }
        }, latencyThreshold + 50)
      }

      this._nprogress = np
      np.init(this)
      np.setComplete = setComplete

      if (applyOnHttp) {
        const axios = options.axios

        if (axios) {
          axios.interceptors.request.use((request) => {
            if (!('showProgressBar' in request)) request.showProgressBar = applyOnHttp
            if (request.showProgressBar) initProgress()
            return request
          }, (error) => {
            return Promise.reject(error)
          })

          axios.interceptors.response.use((response) => {
            if (response.config.showProgressBar) increase()
            return response
          }, (error) => {
            if (error.config && error.config.showProgressBar) increase()
            return Promise.reject(error)
          })
        }
      }

      const router = applyOnRouter && this.$options.router
      if (router) {
        router.beforeEach((route, from, next) => {
          const showProgressBar = 'showProgressBar' in route.meta ? route.meta.showProgressBar : applyOnRouter
          if (showProgressBar && confirmed) {
            initProgress()
            confirmed = false
          }
          next()
        })
        router.afterEach(route => {
          const showProgressBar = 'showProgressBar' in route.meta ? route.meta.showProgressBar : applyOnRouter
          if (showProgressBar) {
            increase()
            confirmed = true
          }
        })
      }
    }
  })
}

function NProgress (options) {
  this.app = null
  this.configure(options || {})
}

NProgress.install = install

Object.assign(NProgress.prototype, nprogress, {
  init (app) {
    this.app = app
  }
})

Vue.use(NProgress, {
  latencyThreshold: 200, // Number of ms before progressbar starts showing, default: 100,
  router: true, // Show progressbar when navigating routes, default: true
  http: true, // Show progressbar when doing Vue.http or axios, default: true
  axios
})

export default new NProgress({
  showSpinner: false
})
