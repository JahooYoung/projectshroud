import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.prototype.axios = axios

const CSRFRegex = /.*csrftoken=([^;.]*).*$/
let userToken = null

axios.interceptors.request.use(config => {
  // only receive json
  config.headers['Content-Type'] = 'application/json'
  // // all status code are valid
  // config.validateStatus = status => status >= 200 && status < 300
  // handle csrftoken
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  const match = document.cookie.match(CSRFRegex)
  config.headers['X-CSRFToken'] = match && match[1]
  // handle authorization
  config.headers['Authorization'] = userToken && `Token ${userToken}`
  return config
})

// Vue.prototype.hasStatus = statusList => {
//   return {
//     validateStatus (status) {
//       return statusList.indexOf(status) !== -1
//     }
//   }
// }

const readLocalStorage = store => {
  if (window.localStorage && window.localStorage.user !== '') {
    store.commit('setUserState', {
      user: window.localStorage.user,
      key: window.localStorage.token
    })
    store.commit('setUserActivation', true)
  }
}

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    userActivated: false,
    isLoading: false
  },
  mutations: {
    setUserState (state, userState) {
      if (userState !== null) {
        state.user = userState.user
        userToken = userState.key
        if (window.localStorage) {
          window.localStorage.user = state.user
          window.localStorage.token = userState.key
        }
      } else {
        state.user = null
        state.userActivated = false
        userToken = null
        if (window.localStorage) {
          window.localStorage.user = ''
          window.localStorage.token = ''
        }
      }
    },
    setUserActivation (state, activated) {
      state.userActivated = activated
    },
    setLoading (state, isLoading) {
      state.isLoading = isLoading
    }
  },
  actions: {

  },
  plugins: [ readLocalStorage ],
  strict: process.env.NODE_ENV !== 'production'
})
