import Vue from 'vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'
import store from './store'

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

Vue.use(Vuelidate)

library.add(faTimesCircle, faCheckCircle)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
