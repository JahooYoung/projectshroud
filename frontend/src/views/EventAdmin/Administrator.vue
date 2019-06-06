<template>
  <b-container>
    <h2>{{ $t('Administrator List') }}</h2>

    <TableLayout
      :item-name="$t('administrator')"
      :refresh="refresh"
      :total-rows="administrators.length"
    >
      <template #buttons>
        <b-button
          id="add-admin-tooltip"
          class="mr-2"
          variant="outline-dark"
          to="attendee"
        >
          {{ $t('Add admin') }}
        </b-button>
        <b-tooltip
          target="add-admin-tooltip"
          :title="$t(`Click '+' in attendee list to make an attendee an admin`)"
        />
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
            <strong>{{ $t('Loading...') }}</strong>
          </div>
        </b-table>
      </template>
    </TableLayout>
  </b-container>
</template>

<script>
import { BButton, BTooltip, BTable, BSpinner } from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'

export default {
  name: 'EventAdminAdministrator',
  components: {
    TableLayout,
    BButton,
    BTooltip,
    BTable,
    BSpinner
  },
  data () {
    return {
      fields: [
        { key: 'realName', label: this.$t('Name') },
        { key: 'mobile', label: this.$t('Mobile') },
        { key: 'email', label: this.$t('Email') }
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
          this.administrators = res.data.map(x => x.userInfo)
        })
    }
  }
}
</script>
