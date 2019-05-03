import Vue from 'vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import NProgress from './plugins/nprogress'
import UserStatus from './plugins/userStatus'

Vue.use(BootstrapVue)

Vue.use(Vuelidate)

library.add(faTimesCircle, faCheckCircle)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(NProgress, {
  latencyThreshold: 200, // Number of ms before progressbar starts showing, default: 100,
  router: true, // Show progressbar when navigating routes, default: true
  http: true, // Show progressbar when doing Vue.http or axios, default: true
  axios
})

Vue.use(UserStatus)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  nprogress: new NProgress({ showSpinner: false }),
  render: h => h(App)
}).$mount('#app')
