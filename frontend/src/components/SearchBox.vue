<template>
  <ais-instant-search :search-client="searchClient" index-name="event_index">
    <ais-search-box show-loading-indicator id="search-box">
      <search-input/>
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
            target="search-box"
            triggers="focus"
            placement="auto"
            :show.sync="query.length"
            ref="popover"
            slot-scope="{ items }"
          >
            <div>
              <div v-if="hits.length > 0">
                <b-list-group>
                  <b-list-group-item
                    v-for="item in items"
                    :key="item.objectId"
                    :to="`/event/${item.id}`"
                  >
                    <h5 v-html="highlight(item._highlightResult.title)">
                    </h5>
                    <p v-html="highlight(item._snippetResult.description)">
                    </p>
                  </b-list-group-item>
                </b-list-group>
                <ais-pagination />
              </div>
              <div v-else>
                There are no hits found for: <q>{{query}}</q>
              </div>
              <ais-powered-by/>
            </div>
          </b-popover>
        </ais-hits>
        <div v-else>
        </div>
      </template>
    </ais-state-results>
    <ais-configure
      :attributesToSnippet="['description']"
      :hits-per-page.camel="5"
      snippetEllipsisText="..."
    />
  </ais-instant-search>
</template>

<script>
import algoliasearch from 'algoliasearch/lite'
import 'instantsearch.css/themes/algolia-min.css'
import SearchInput from './SearchInput'

export default {
  components: {
    SearchInput
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
    printHit (hits) {
      console.log(hits)
      return true
    },
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
