<template>
  <b-container>
    <h2>Administrator List</h2>

    <TableLayout
      item-name="administrator"
      :refresh="refresh"
      :total-rows="administrators.length"
    >
      <template #buttons>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          Export
        </b-button>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          Add administrator
        </b-button>
      </template>

      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="administrators"
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
        </b-table>
      </template>
    </TableLayout>
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'

export default {
  name: 'EventAdminAdministrator',
  components: {
    TableLayout
  },
  data () {
    return {
      fields: [
        { key: 'real_name', label: 'Name' },
        { key: 'mobile', label: 'Mobile' },
        { key: 'email', label: 'Email' }
      ],
      administrators: []
    }
  },
  watch: {
    '$route': 'refresh'
  },
  created () {
    this.refresh()
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/' + this.$route.params.id + '/admins/')
        .then(res => {
          this.administrators = res.data.map(x => x.user_info)
        })
    }
  }
}
</script>
