<template>
  <b-container>
    <h2>Event List</h2>

    <TableLayout
      item-name="event"
      :refresh="refresh"
      :total-rows="events.length"
    >
      <template #buttons>
        <b-button
          class="mr-2"
          variant="outline-dark"
          to="/event/new"
        >
          New Event
        </b-button>
      </template>

      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="events"
          :fields="fields"
          primary-key="id"
        >
          <div
            slot="table-busy"
            class="text-center text-primary my-2"
          >
            <b-spinner class="align-middle mr-2" />
            <strong>Loading...</strong>
          </div>

          <template #title="row">
            <b-link :to="'/event/' + row.item.id">
              {{ row.value }}
            </b-link>
          </template>
        </b-table>
      </template>
    </TableLayout>
  </b-container>
</template>

<script>
import { BButton, BTable, BLink } from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'

const fields = Object.freeze([
  {
    key: 'title',
    label: 'Title'
  },
  {
    key: 'startTime',
    sortable: true,
    formatter: value => value.toLocaleString()
  },
  {
    key: 'location',
    label: 'Location'
  },
  {
    key: 'hostDisplayInfo',
    label: 'Host'
  },
  {
    key: 'requireApprove',
    formatter: value => value ? 'Yes' : 'No'
  }
])

export default {
  name: 'EventList',
  components: {
    TableLayout,
    BButton,
    BTable,
    BLink
  },
  data () {
    return {
      fields,
      events: []
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/')
        .then(res => {
          this.events = res.data
        })
    }
  }
}
</script>
