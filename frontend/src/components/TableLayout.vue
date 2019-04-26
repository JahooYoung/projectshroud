<template>
  <b-row>
    <b-input-group class="w-25 my-3">
      <b-form-input
        v-model="filter"
        :placeholder="`Search ${itemName}`"
      />
      <b-input-group-append>
        <b-button
          :disabled="!filter"
          @click="filter = ''"
        >
          Clear
        </b-button>
      </b-input-group-append>
    </b-input-group>

    <div class="ml-auto my-3">
      <slot name="buttons" />

      <b-button
        variant="outline-dark"
        :disabled="isLoading"
        @click="refresh"
      >
        Refresh
      </b-button>
    </div>

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
export default {
  name: 'TableLayout',
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
