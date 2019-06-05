import Vue from 'vue'
import { ToastPlugin } from 'bootstrap-vue'

Vue.use(ToastPlugin)

const install = _Vue => {
  if (install.installed) {
    // Only install once
    /* istanbul ignore next */
    return
  }
  install.installed = true

  // Add our instance mixin
  _Vue.mixin({
    methods: {
      toastSuccess (msg, title, to) {
        this.$root.$bvToast.toast(msg, {
          title: title || 'Success',
          variant: 'default',
          autoHideDelay: 3000,
          solid: true,
          to: to
        })
      },
      toastWarning (msg, title, to) {
        this.$root.$bvToast.toast(msg, {
          title: title || 'Warning',
          variant: 'warning',
          autoHideDelay: 4000,
          solid: true,
          to: to
        })
      },
      toastError (msg, title, to) {
        this.$root.$bvToast.toast(msg, {
          title: title || 'Error',
          variant: 'danger',
          autoHideDelay: 5000,
          solid: true,
          to: to
        })
      }
    }
  })
}

install.installed = false

export default {
  install
}
