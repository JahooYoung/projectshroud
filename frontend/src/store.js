import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

axios.interceptors.request.use(config => {
  // only receive json
  config.headers['Content-Type'] = 'application/json'
  // all status code are valid
  config.validateStatus = status => true
  // handle csrftoken
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  const regex = /.*csrftoken=([^;.]*).*$/
  config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]
  return config
})

Vue.use(Vuex)

const readLocalStorage = store => {
  if (window.localStorage && window.localStorage.user) {
    store.commit('setUserState', {
      user: window.localStorage.user,
      key: window.localStorage.token
    })
  }
}

export default new Vuex.Store({
  state: {
    user: null,
    tokenInterceptor: null
  },
  mutations: {
    setUserState (state, userState) {
      if (userState != null) {
        state.user = userState.user
        state.tokenInterceptor = axios.interceptors.request.use(config => {
          config.headers['Authorization'] = 'Token ' + userState.key
          return config
        })
        if (window.localStorage) {
          window.localStorage.user = state.user
          window.localStorage.token = userState.key
        }
      } else {
        state.user = null
        if (state.tokenInterceptor != null) {
          axios.interceptors.request.eject(state.tokenInterceptor)
        }
        if (window.localStorage) {
          window.localStorage.user = null
          window.localStorage.token = null
        }
      }
    }
  },
  actions: {

  },
  plugins: [ readLocalStorage ],
  strict: process.env.NODE_ENV !== 'production'
})
