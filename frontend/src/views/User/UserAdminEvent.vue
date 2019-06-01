<template>
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
          sort-by="startTime"
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
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'

export default {
  name: 'UserAdminEvent',
  components: {
    TableLayout
  },
  data () {
    return {
      fields: [
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'startTime',
          label: 'Start Time',
          sortable: true,
          formatter: value => value.toLocaleString()
        },
        {
          key: 'attendeeCount',
          label: 'No. Attendee',
          sortable: true
        },
        {
          key: 'applicantCount',
          label: 'No. Applicant',
          sortable: true
        },
        {
          key: 'actions',
          label: 'Actions'
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