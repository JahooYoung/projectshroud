<template>
  <div>
    <b-container>
      <h2>Admin Events</h2>

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
            :tbody-tr-class="rowClass"
            primary-key="id"
            sort-by="start_time"
            caption="Blue represents the event is checking in."
          >
            <div
              slot="table-busy"
              class="text-center text-primary my-2"
            >
              <b-spinner class="align-middle mr-2" />
              <strong>Loading...</strong>
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
                Manage
              </b-button>
            </template>
          </b-table>
        </template>
      </TableLayout>
    </b-container>
  </div>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'

export default {
  components: {
    TableLayout
  },
  data () {
    return {
      fields: [
        'title',
        {
          key: 'start_time',
          label: 'Start Time',
          sortable: true,
          formatter: value => new Date(value).toLocaleString()
        },
        {
          key: 'actions'
        }
      ],
      events: []
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/admins/')
        .then(res => {
          console.log(res.data[0].event_info)
          this.events = res.data.map(x => x.event_info)
        })
    },
    rowClass (item, type) {
      if (item.checkin_enabled) {
        return 'table-primary'
      }
    }
  }
}
</script>
