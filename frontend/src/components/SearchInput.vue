<template>
  <b-nav-form>
    <b-form-input
      class="mr-sm-2"
      type="search"
      placeholder="Search"
      v-model="query"
    />
  </b-nav-form>
</template>

<script>
import { connectSearchBox } from 'instantsearch.js/es/connectors'
import { createWidgetMixin } from 'vue-instantsearch'
import _ from 'lodash'

export default {
  mixins: [createWidgetMixin({ connector: connectSearchBox })],
  props: {
    delay: {
      type: Number,
      default: 500,
      required: false
    }
  },
  data () {
    return {
      localQuery: '',
      refine: null
    }
  },
  methods: {
  },
  computed: {
    query: {
      get () {
        return this.localQuery
      },
      set (val) {
        this.localQuery = val
        if (this.refine == null) {
          this.refine = _.debounce(() => {
            this.state.refine(this.localQuery)
          }, 300)
        }
        this.refine()
      }
    }
  }
}
</script>
