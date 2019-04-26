<template>
  <ais-instant-search
    :search-client="searchClient"
    index-name="event_index"
  >
    <ais-search-box id="search-box">
      <search-input />
    </ais-search-box>
    <!-- <ais-search-box>
      <div slot-scope="{ currentRefinement, isSearchStalled, refine }">
        <b-nav-form>
          <b-form-input
            class="mr-sm-2"
            type="search"
            placeholder="Search"
            v-model="currentRefinement"
            @input="refine($event.currentTarget.value)"
          />
          <span :hidden="!isSearchStalled">Loading...</span>
        </b-nav-form>
      </div>
    </ais-search-box> -->
    <ais-state-results>
      <template slot-scope="{ query, hits }">
        <ais-hits v-if="query.length > 0">
          <b-popover
            ref="popover"
            slot-scope="{ items }"
            target="search-box"
            triggers="focus"
            placement="auto"
            :show.sync="query.length"
          >
            <div>
              <div v-if="hits.length > 0">
                <b-list-group>
                  <b-list-group-item
                    v-for="item in items"
                    :key="item.objectId"
                    :to="`/event/${item.id}`"
                  >
                    <h5 v-html="highlight(item._highlightResult.title)" />
                    <p v-html="highlight(item._snippetResult.description)" />
                  </b-list-group-item>
                </b-list-group>
                <ais-pagination />
              </div>
              <div v-else>
                There are no hits found for: <q>{{ query }}</q>
              </div>
              <ais-powered-by />
            </div>
          </b-popover>
        </ais-hits>
        <div v-else />
      </template>
    </ais-state-results>
    <ais-configure
      :attributes-to-snippet.camel="['description']"
      :hits-per-page.camel="5"
      :snippet-ellipsis-text.camel="'...'"
    />
  </ais-instant-search>
</template>

<script>
import algoliasearch from 'algoliasearch/lite'
import 'instantsearch.css/themes/algolia-min.css'
import {
  AisInstantSearch, AisSearchBox, AisStateResults, AisConfigure,
  AisHits, AisPoweredBy, AisPagination
} from 'vue-instantsearch'
import SearchInput from './SearchInput'

export default {
  name: 'SearchBox',
  components: {
    SearchInput,
    AisInstantSearch,
    AisSearchBox,
    AisStateResults,
    AisConfigure,
    AisHits,
    AisPoweredBy,
    AisPagination
  },
  data () {
    return {
      searchClient: algoliasearch(
        'WN4Q0PFNA4',
        '856d81f42e715a208a22112291343573'
      )
    }
  },
  methods: {
    highlight (obj) {
      return obj.value
        .replace(/<mark>/g, `<span class="search-highlight">`)
        .replace(/<\/mark>/g, `</span>`)
    }
  }
}
</script>

<style>
.search-highlight {
  color: red
}
</style>
