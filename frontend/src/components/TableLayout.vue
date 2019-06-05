<template>
  <b-row>
    <b-col
      cols="12"
      md="4"
      class="px-0 my-3"
    >
      <b-input-group>
        <b-form-input
          v-model="filter"
          :placeholder="$t(`Search `) +`${itemName}`"
        />
        <b-input-group-append>
          <b-button
            size="sm"
            :disabled="!filter"
            @click="filter = ''"
          >
            {{ $t('Clear') }}
          </b-button>
        </b-input-group-append>
      </b-input-group>
    </b-col>
    <b-col
      cols="12"
      md="8"
      class="px-0 my-3"
      align="right"
    >
      <slot name="buttons" />

      <b-button
        variant="outline-dark"
        :disabled="isLoading"
        @click="refresh"
      >
        {{ $t('Refresh') }}
      </b-button>
    </b-col>

    <slot
      :id="itemName + '-table-layout'"
      striped
      hover
      show-empty
      responsive
      :filter="filter"
      :busy="isLoading"
      :per-page="perPage"
      :current-page="currentPage"
      :empty-text="$t('There are no records to show')"
      :empty-filtered-text="$t('There are no records matching your request')"
    />

    <b-col cols="12">
      <div class="mt-3">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="center"
          :aria-controls="itemName + '-table-layout'"
        />
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { BInputGroup, BInputGroupAppend, BFormInput, BButton, BPagination } from 'bootstrap-vue'

export default {
  name: 'TableLayout',
  components: {
    BInputGroup,
    BInputGroupAppend,
    BFormInput,
    BButton,
    BPagination
  },
  props: {
    itemName: {
      type: String,
      required: true
    },
    refresh: {
      type: Function,
      required: true
    },
    perPage: {
      type: Number,
      default: 10
    },
    totalRows: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      filter: '',
      currentPage: 1
    }
  }
}
</script>
