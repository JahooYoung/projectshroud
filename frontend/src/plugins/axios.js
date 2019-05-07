import Vue from 'vue'
import _axios from 'axios'
import store from './store'

const CSRFRegex = /.*csrftoken=([^;.]*).*$/
const CSRFMatch = document.cookie.match(CSRFRegex)

const axios = _axios.create({
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': CSRFMatch && CSRFMatch[1]
  }
})

function transformDate2String (obj) {
  if (typeof obj !== 'object' || !obj) {
    return obj
  }
  for (let key in obj) {
    if (key.endsWith('time') && obj[key] instanceof Date) {
      obj[key] = obj[key].toISOString()
    } else if (typeof obj[key] === 'object') {
      obj[key] = transformDate2String(obj[key])
    }
  }
  return obj
}

function transformString2Date (obj) {
  if (typeof obj !== 'object' || !obj) {
    return obj
  }
  for (let key in obj) {
    if (key.endsWith('time') && typeof obj[key] === 'string') {
      obj[key] = new Date(obj[key])
    } else if (typeof obj[key] === 'object') {
      obj[key] = transformString2Date(obj[key])
    }
  }
  return obj
}

axios.interceptors.request.use(config => {
  // handle authorization
  if (store.state.userToken) {
    config.headers['Authorization'] = `Token ${store.state.userToken}`
  }

  config.data = transformDate2String(config.data)
  return config
})

axios.interceptors.response.use(res => {
  res.data = transformString2Date(res.data)
  return res
})

Vue.prototype.axios = axios

export default axios
