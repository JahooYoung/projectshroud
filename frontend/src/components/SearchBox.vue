<template>
  <b-nav-form>
    <type-ahead
      v-model="query"
      placeholder="Search events..."
      no-result-text="No result matching your query"
      searching-text="Just a moment..."
      select-first
      :min-chars="1"
      :delay-time="250"
      :fetch="fetch"
      :get-response="getResponse"
      :highlighting="highlighting"
      :on-hit="onHit"
      class="mr-sm-2"
      style="width: 20em"
    />
  </b-nav-form>
</template>

<script>
import algoliasearch from 'algoliasearch/lite'
import TypeAhead from './TypeAhead.vue'

export default {
  name: 'SearchBox',
  components: {
    TypeAhead
  },
  data () {
    return {
      query: '',
      index: algoliasearch(
        'WN4Q0PFNA4',
        '856d81f42e715a208a22112291343573'
      ).initIndex('event_index')
    }
  },
  methods: {
    fetch () {
      return this.index.search({
        query: this.query,
        attributesToSnippet: ['description'],
        snippetEllipsisText: '...'
      })
    },
    getResponse (content) {
      return content.hits
    },
    replaceTag (value) {
      return value
        .replace(/<em>/g, `<span class="search-highlight">`)
        .replace(/<\/em>/g, `</span>`)
    },
    highlighting (item) {
      return this.replaceTag(item._highlightResult.title.value)
      // const title = this.replaceTag(item._highlightResult.title.value)
      // const description = this.replaceTag(item._snippetResult.description.value)
      // return `<h5>${title}</h5>${description}`
    },
    onHit (item, self, id) {
      if (id !== undefined) {
        this.$router.push(`/event/${item.id}`)
      }
    }
  }
}
</script>

<style>
.search-highlight {
  color: #dc3545
}
</style>
