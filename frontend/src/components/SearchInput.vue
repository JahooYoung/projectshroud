<template>
  <b-nav-form>
    <b-spinner
      v-if="state.isSearchStalled"
      variant="light"
      label="Spinning"
      class="mr-sm-2"
    />
    <b-form-input
      class="mr-sm-2"
      type="search"
      placeholder="Search..."
      v-model="query"
    />
  </b-nav-form>
</template>

<script>
import { connectSearchBox } from 'instantsearch.js/es/connectors'
import { createWidgetMixin } from 'vue-instantsearch'
import _ from 'lodash/function'

export default {
  mixins: [createWidgetMixin({ connector: connectSearchBox })],
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
