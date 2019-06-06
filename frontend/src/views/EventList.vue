<template>
  <b-container>
    <h2>{{ $t('Event List') }}</h2>

    <TableLayout
      :item-name="$t('Event')"
      :refresh="refresh"
      :total-rows="events.length"
    >
      <template #buttons>
        <b-button
          class="mr-2"
          variant="outline-dark"
          to="/event/new"
        >
          {{ $t('New Event') }}
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
            <strong>{{ $t('Loading...') }}</strong>
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
      events: []
    }
  },
  computed: {
    fields () {
      return [
        {
          key: 'title',
          label: this.$t('Title')
        },
        {
          key: 'startTime',
          label: this.$t('Start time'),
          sortable: true,
          formatter: value => value.toLocaleString()
        },
        {
          key: 'location',
          label: this.$t('Location')
        },
        {
          key: 'hostDisplayInfo',
          label: this.$t('Host')
        },
        {
          key: 'requireApprove',
          label: this.$t('Approve required?'),
          formatter: value => value ? this.$t('Yes') : this.$t('No')
        }
      ]
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
