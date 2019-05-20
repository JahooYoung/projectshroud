<template>
  <flat-pickr
    :value="value"
    class="form-control"
    :config="{
      enableTime: true,
      time_24hr: true,
      locale
    }"
    @on-change="update"
  />
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/themes/material_blue.css'
import zh from 'flatpickr/dist/l10n/zh'

export default {
  name: 'TimePicker',
  components: {
    flatPickr
  },
  props: {
    value: Date
  },
  computed: {
    locale () {
      if (this.$i18n.locale === 'zh') {
        return zh.zh
      } else {
        return null
      }
    }
  },
  methods: {
    update (value) {
      value = new Date(value)
      if (this.value - value !== 0) {
        this.$emit('input', value)
      }
    }
  }
}
</script>
