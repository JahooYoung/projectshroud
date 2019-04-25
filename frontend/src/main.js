import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import NProgress from './nprogress'

import BootstrapVue from 'bootstrap-vue'
// import BVConfig from 'bootstrap-vue/es/bv-config'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimesCircle, faCheckCircle } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import InstantSearch from 'vue-instantsearch'

Vue.use(InstantSearch)

// Vue.use(BVConfig, {
//   BToast: {
//     autoHideDelay: 3000,
//     solid: true
//   }
// })
Vue.use(BootstrapVue)

library.add(faTimesCircle, faCheckCircle)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(NProgress, {
  latencyThreshold: 0, // Number of ms before progressbar starts showing, default: 100,
  router: true, // Show progressbar when navigating routes, default: true
  http: true, // Show progressbar when doing Vue.http, default: true
  showSpinner: false
})

Vue.config.productionTip = false

new Vue({
  router,
  store,
  nprogress: new NProgress(),
  render: h => h(App)
}).$mount('#app')
