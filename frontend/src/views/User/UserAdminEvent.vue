<template>
  <b-container>
    <h2>{{ $t('Admin Events') }}</h2>

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
          :tbody-tr-class="rowClass"
          primary-key="id"
          sort-by="startTime"
        >
          <div
            slot="table-busy"
            class="text-center text-primary my-2"
          >
            <b-spinner class="align-middle mr-2" />
            <strong>{{ $t('Loading...') }}</strong>
          </div>

          <template
            slot="title"
            slot-scope="row"
          >
            <b-link :to="'/event/' + row.item.id">
              {{ row.value }}
            </b-link>
          </template>

          <template
            slot="actions"
            slot-scope="row"
          >
            <b-button
              variant="dark"
              size="sm"
              :to="`/event/${row.item.id}/admin`"
            >
              {{ $t('Manage') }}
            </b-button>
          </template>
        </b-table>
      </template>
    </TableLayout>
  </b-container>
</template>

<script>
import { BButton, BTable, BLink, BSpinner } from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'

export default {
  name: 'UserAdminEvent',
  components: {
    TableLayout,
    BButton,
    BTable,
    BLink,
    BSpinner
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
          key: 'attendeeCount',
          label: this.$t('No. Attendee'),
          sortable: true
        },
        {
          key: 'applicantCount',
          label: this.$t('No. Applicant'),
          sortable: true
        },
        {
          key: 'actions',
          label: this.$t('Actions')
        }
      ]
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/admins/')
        .then(res => {
          this.events = res.data.map(x => x.eventInfo)
        })
    },
    rowClass (item, type) {
      if (item && item.checkinEnabled) {
        return 'table-primary'
      }
    }
  }
}
</script>
