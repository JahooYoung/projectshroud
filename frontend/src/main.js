import Vue from 'vue'
import App from './App.vue'
import router from './plugins/router'
import store from './plugins/store'
import i18n from './plugins/i18n'
import nprogress from './plugins/nprogress'
import UserStatus from './plugins/userStatus'
import bvToastHelper from './plugins/bvToastHelper'

import BootstrapVue from 'bootstrap-vue'
import './style.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(UserStatus)
Vue.use(bvToastHelper)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  nprogress,
  i18n,
  render: h => h(App)
}).$mount('#app')
