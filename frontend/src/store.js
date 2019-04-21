import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

let userToken = ''

axios.interceptors.request.use(config => {
  // only receive json
  config.headers['Content-Type'] = 'application/json'
  // all status code are valid
  config.validateStatus = status => true
  // handle csrftoken
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  const regex = /.*csrftoken=([^;.]*).*$/
  config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]
  if (userToken !== '') {
    config.headers['Authorization'] = 'Token ' + userToken
  }
  return config
})

Vue.use(Vuex)

const readLocalStorage = store => {
  if (window.localStorage && window.localStorage.user !== '') {
    store.commit('setUserState', {
      user: window.localStorage.user,
      key: window.localStorage.token
    })
    axios.get('/api/dummy/')
      .then(res => {
        if (res.status !== 200) {
          store.commit('setUserState', null)
          alert('Please login agian!')
        }
      })
      .catch(err => {
        console.log(err)
        store.commit('setUserState', null)
        alert('Please login agian!')
      })
  }
}

export default new Vuex.Store({
  state: {
    user: null
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
        userToken = ''
        if (window.localStorage) {
          window.localStorage.user = ''
          window.localStorage.token = ''
        }
      }
    }
  },
  actions: {

  },
  plugins: [ readLocalStorage ],
  strict: process.env.NODE_ENV !== 'production'
})
