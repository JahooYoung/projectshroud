import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

axios.interceptors.request.use((config) => {
  config.headers['Content-Type'] = 'application/json'
  // handle csrftoken
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  const regex = /.*csrftoken=([^;.]*).*$/
  config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]
  return config
})

Vue.use(Vuex)

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
      } else {
        state.user = null
        if (state.tokenInterceptor != null) {
          axios.interceptors.request.eject(state.tokenInterceptor)
        }
      }
    }
  },
  actions: {

  }
})
