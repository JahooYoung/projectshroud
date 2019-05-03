import Vue from 'vue'
import VueI18n from 'vue-i18n'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import NProgress from './plugins/nprogress'
import UserStatus from './plugins/userStatus'

Vue.use(VueI18n)

Vue.use(BootstrapVue)

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
