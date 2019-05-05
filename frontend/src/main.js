import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import axios from 'axios'

import BootstrapVue from 'bootstrap-vue'
import './style.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import NProgress from './plugins/nprogress'
import UserStatus from './plugins/userStatus'

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
  i18n,
  render: h => h(App)
}).$mount('#app')
