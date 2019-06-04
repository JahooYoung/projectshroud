<template>
  <b-container>
    <h2>{{ $t('Attendee List') }}</h2>

    <b-progress
      class="my-3"
      :max="attendee.length"
      show-value
    >
      <b-progress-bar
        :value="attendee.filter(x => x.checkedIn).length"
        variant="success"
      />
      <b-progress-bar
        :value="attendee.filter(x => !x.checkedIn && x.approved).length"
        variant="primary"
      />
    </b-progress>

    <TableLayout
      :item-name="$t('attendee')"
      :refresh="refresh"
      :total-rows="attendee.length"
    >
      <template #buttons>
        <b-dropdown
          split
          :text="$t('Import')"
          :ok-title="$t('Accept')"
          :cancel-title="$t('Reject')"
          variant="outline-dark"
          class="mr-2"
          @click="importExcel"
        >
          <b-dropdown-item @click="downloadTemplate">
            {{ $t('Download template') }}
          </b-dropdown-item>
        </b-dropdown>
        <b-button
          class="mr-2"
          variant="outline-dark"
          @click="exportExcel"
        >
          {{ $t('Export') }}
        </b-button>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          {{ $t('Add attendee') }}
        </b-button>
      </template>

      <template v-slot="config">
        <b-table
          v-bind="config"
          :items="attendee"
          :fields="fields"
          primary-key="userInfo.id"
        >
          <template #transportInfo="row">
            <div v-if="row.value">
              {{ row.value.arrivalStation }} <br>
              {{ row.value.arrivalTime.toLocaleString() }}
            </div>
            <div v-else>
              {{ $t('None') }}
            </div>
          </template>

          <template #approved="row">
            <font-awesome-icon
              v-if="row.value"
              icon="check"
              :style="{ color: 'green' }"
            />
            <b-button
              v-else
              size="sm"
              variant="warning"
              @click="approve(row)"
            >
              {{ $t('Pending') }}
            </b-button>
          </template>

          <template
            slot="checkedIn"
            slot-scope="row"
          >
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="times"
              :style="{ color: 'red' }"
            />
            <!-- <b-popover
              :target="'checkin-popover-' + row.item.userInfo.id"
              triggers="hover focus"
            >
              <template slot="title">
                Manually check in (click to keep) (not impl.)
              </template>
              <b-button
                variant="success"
                :disabled="row.value || true"
                @click="manualCheckIn(row.item)"
              >
                Manually check in
              </b-button>
            </b-popover> -->
          </template>

          <template
            slot="isAdmin"
            slot-scope="row"
          >
            <font-awesome-icon
              v-if="row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="check"
              :style="{ color: 'green' }"
            />
            <font-awesome-icon
              v-else
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="times"
              :style="{ color: 'red' }"
            />
            <font-awesome-icon
              v-if="!row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="plus"
              :style="{ color: '#2196F3' }"
              class="ml-3"
              @click="assignAdmin(row.item)"
            />
          </template>
        </b-table>
      </template>
    </TableLayout>

    <b-modal
      ref="modal-approve"
      cancel-variant="danger"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <template #modal-title>
        {{ modalData && modalData.userInfo.realName }}{{ $t(`'s application`) }}
      </template>
      <h5>{{ $t('Application Text:') }}</h5>
      {{ modalData && (modalData.applicationText || $t('Empty')) }}
    </b-modal>

    <b-modal
      ref="modal-add-admin"
      :title="$t('Confirm')"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <p class="my-3">
        {{ $t('Are you sure to add') + newAdminName + $t('as an administrator?') }} <br>
        <b>{{ $t('Warning:') }}</b> {{ $t('You cannot undo this operation!') }}
      </p>
    </b-modal>

    <b-modal
      ref="modal-import-excel"
      :title="$t('Import excel (.xlsx)')"
      :ok-title="$t('OK')"
      :cancel-title="$t('Cancel')"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <b-form-file
        v-model="excelFile"
        :state="Boolean(excelFile)"
        :browse-text="$t('Brouse')"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        :placeholder="$t('Choose a file...')"
        :drop-placeholder="$t('Drop file here...')"
      />
    </b-modal>

    <b-modal
      ref="modal-import-result"
      :title="$t('Import result')"
      ok-only
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <p class="my-3">
        <b>{{ $t('No. successful users:') }}</b> {{ importResult.successCount }} <br>
        <b>{{ $t('No. failed users:') }}</b> {{ importResult.failCount }} <br>
        <b>{{ $t('No. new registered users:') }}</b> {{ importResult.userCount }}
      </p>
    </b-modal>
  </b-container>
</template>

<script>
import TableLayout from '@/components/TableLayout.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimes, faCheck, faPlus)

export default {
  name: 'EventAdminAttendee',
  components: {
    TableLayout,
    FontAwesomeIcon
  },
  data () {
    return {
      fields: [
        {
          key: 'userInfo.realName',
          label: this.$t('Name')
        },
        {
          key: 'userInfo.mobile',
          label: this.$t('Mobile')
        },
        // {
        //   key: 'dateRegistered',
        //   label: 'Registered Time',
        //   formatter: t => t.toLocaleString()
        // },
        {
          key: 'transportInfo',
          label: this.$t('Arrival Info'),
          sortable: true
        },
        {
          key: 'approved',
          label: this.$t('Approval Status'),
          sortable: true
        },
        {
          key: 'checkedIn',
          label: this.$t('Checked-in Status'),
          sortable: true
        },
        {
          key: 'isAdmin',
          label: this.$t('Is Admin'),
          sortable: true
        }
      ],
      attendee: [],
      modalCallback: null,
      modalData: null,
      newAdminName: '',
      excelFile: null,
      importResult: {
        successCount: 0,
        failCount: 0,
        userCount: 0
      }
    }
  },
  computed: {
    eventId () {
      return this.$route.params.id
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    async refresh () {
      const res = await this.axios.get(`/api/event/${this.eventId}/attendee/`)
      this.attendee = res.data
    },
    // manualCheckIn (rowItem) {
    //   // Todo
    // },
    showModal (modal) {
      return new Promise(resolve => {
        this.modalCallback = answer => {
          this.modalCallback = null
          resolve(answer)
        }
        this.$refs[modal].show()
      })
    },
    async assignAdmin (rowItem) {
      this.newAdminName = rowItem.userInfo.realName
      const answer = await this.showModal('modal-add-admin')
      if (answer) {
        try {
          await this.axios.post('/api/assignadmin/', {
            userId: rowItem.userInfo.id,
            eventId: this.eventId
          })
          rowItem.isAdmin = true
        } catch (err) {
          this.toastError(this.$t('Failed to assign admin'))
        }
      }
    },
    async approve (row) {
      this.modalData = row.item
      const answer = await this.showModal('modal-approve')
      if (answer !== null) {
        const user = row.item.userInfo.realName
        try {
          await this.axios.post(`/api/approve/`, {
            userId: row.item.userInfo.id,
            eventId: this.eventId,
            approve: answer
          })
          if (answer) {
            row.item.approved = true
            this.toastSuccess(this.$t('Succeed to approve user ', [user]))
          } else {
            this.attendee = this.attendee.filter(
              x => x.userInfo.id !== row.item.userInfo.id
            )
            this.toastSuccess(this.$t('Succeed to reject user ', [user]))
          }
        } catch (err) {
          if (answer) {
            this.toastError(this.$t('Failed to approve user ', [user]))
          } else {
            this.toastError(this.$t('Failed to reject user ', [user]))
          }
        }
      }
    },
    async download (url) {
      const res = await this.axios.get(url, {
        responseType: 'blob'
      })
      const blob = new Blob([res.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      })
      const a = document.createElement('a')
      a.download = decodeURI(res.headers['content-disposition'].match(/^.*filename=(.*)$/)[1])
      a.href = URL.createObjectURL(blob)
      a.click()
      URL.revokeObjectURL(a.href)
    },
    async exportExcel () {
      this.download(`/api/event/${this.eventId}/export/`)
    },
    async downloadTemplate () {
      this.download(`/api/download/import/`)
    },
    async importExcel () {
      const answer = await this.showModal('modal-import-excel')
      if (answer) {
        const formData = new FormData()
        formData.append('file', this.excelFile)
        try {
          const res = await this.axios.post(`/api/event/${this.eventId}/import/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          this.importResult = res.data
          this.showModal('modal-import-result')
          this.refresh()
        } catch (err) {
          if (err.needHandle) {
            this.toastError(this.$t('Failed to import! Please check your file conform to the template.'))
          }
        }
      }
    }
  }
}
</script>
