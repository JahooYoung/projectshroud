<template>
  <div>
    <h2>Administrator List</h2>
    <b-container>
      <b-row>
        <b-col
          md="4"
          class="my-1"
        >
          <b-input-group>
            <b-input-group-text slot="prepend">
              Filter
            </b-input-group-text>
            <b-form-input
              v-model="filter"
              placeholder="Type to Search"
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
        </b-col>
        <b-col
          offset-md="3"
          md="1"
          class="my-1"
        >
          <b-button
            variant="outline-info"
            href="#"
          >
            Export
          </b-button>
        </b-col>
        <b-col
          offset-md="0"
          md="2"
          class="my-1"
        >
          <b-button
            variant="outline-info"
            href="#"
          >
            Add administrator
          </b-button>
        </b-col>
        <b-col
          offset-md="0"
          md="1"
          class="my-1"
        >
          <b-button
            variant="outline-info"
            @click="refresh"
            :disabled="isLoading"
          >
            Refresh
          </b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table
      striped
      hover
      show-empty
      :fields="fields"
      primary-key="user_info.id"
      :items="administrators"
      :busy="isLoading"
      :filter="filter"
    >
      <div
        slot="table-busy"
        class="text-center text-danger my-2"
      >
        <b-spinner class="align-middle" />
        <strong>Loading...</strong>
      </div>

      <template
        slot="actions"
        slot-scope="row"
      >
        <b-button
          size="sm"
          @click="row.toggleDetails"
        >
          {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
        </b-button>
      </template>

      <template
        slot="row-details"
        slot-scope="row"
      >
        <b-card>
          <ul>
            <li
              v-for="(value, key) in row.item"
              :key="key"
            >
              {{ key }}: {{ value }}
            </li>
          </ul>
        </b-card>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      fields: [
        { key: 'user_info.real_name', label: 'Name' },
        { key: 'user_info.mobile', label: 'Mobile' },
        { key: 'user_info.email', label: 'Email' }
      ],
      filter: null,
      administrators: []
    }
  },
  created () {
    this.refresh()
  },
  watch: {
    '$route': 'refresh'
  },
  methods: {
    refresh () {
      this.axios.get('/api/event/' + this.$route.params.id + '/admins/')
        .then(res => {
          this.administrators = res.data
        })
    }
  }
}
</script>
