<template>
  <b-container>
    <h2>Attendee List</h2>

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

    <b-alert
      :show="Boolean(importSocket)"
      variant="dark"
      align="left"
      dismissible
      @dismissed="closeSocket"
    >
      <h6>
        {{ importResult.finished ? 'Import finished' : 'Importing...' }}
        (
        Total: {{ importResult.total }}
        Success: {{ importResult.successCount }},
        Failure: {{ importResult.failCount }},
        New registered user: {{ importResult.userCount }}
        )
      </h6>
      <b-progress
        :max="importResult.total"
        height="0.4rem"
      >
        <b-progress-bar
          :value="importResult.successCount"
          :animated="!importResult.finished"
          variant="success"
          striped
        />
        <b-progress-bar
          :value="importResult.failCount"
          :animated="!importResult.finished"
          variant="warning"
          striped
        />
      </b-progress>
    </b-alert>

    <TableLayout
      item-name="attendee"
      :refresh="refresh"
      :total-rows="attendee.length"
    >
      <template #buttons>
        <b-dropdown
          split
          text="Import"
          variant="outline-dark"
          class="mr-2"
          @click="importExcel"
        >
          <b-dropdown-item @click="downloadTemplate">
            Download template
          </b-dropdown-item>
        </b-dropdown>
        <b-button
          class="mr-2"
          variant="outline-dark"
          @click="exportExcel"
        >
          Export
        </b-button>
        <b-button
          class="mr-2"
          variant="outline-dark"
          href="#"
        >
          Add attendee
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
              None
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
              See detail
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
      ok-title="Accept"
      cancel-title="Reject"
      cancel-variant="danger"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <template #modal-title>
        {{ modalData && modalData.userInfo.realName }}'s application
      </template>
      <h5>Application Text:</h5>
      {{ modalData && (modalData.applicationText || 'Empty') }}
    </b-modal>

    <b-modal
      ref="modal-add-admin"
      title="Confirm"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <p class="my-3">
        Are you sure to add {{ newAdminName }} as an administrator? <br>
        <b>Warning:</b> You cannot undo this operation!
      </p>
    </b-modal>

    <b-modal
      ref="modal-import-excel"
      title="Import excel (.xlsx)"
      :ok-disabled="!excelFile"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <b-form-file
        v-model="excelFile"
        :state="Boolean(excelFile)"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        placeholder="Choose a file..."
        drop-placeholder="Drop file here..."
      />
    </b-modal>
  </b-container>
</template>

<script>
import {
  BProgress, BProgressBar, BAlert, BDropdown, BDropdownItem, BButton, BTable,
  BFormFile
} from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'
import { transformJSON2Object } from '@/plugins/axios.js'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimes, faCheck, faPlus)

export default {
  name: 'EventAdminAttendee',
  components: {
    TableLayout,
    FontAwesomeIcon,
    BProgress,
    BProgressBar,
    BAlert,
    BDropdown,
    BDropdownItem,
    BButton,
    BTable,
    BFormFile
  },
  data () {
    return {
      fields: [
        {
          key: 'userInfo.realName',
          label: 'Name'
        },
        {
          key: 'userInfo.mobile',
          label: 'Mobile'
        },
        // {
        //   key: 'dateRegistered',
        //   label: 'Registered Time',
        //   formatter: t => t.toLocaleString()
        // },
        {
          key: 'transportInfo',
          label: 'Arrival Info',
          sortable: true
        },
        {
          key: 'approved',
          label: 'Approve',
          sortable: true
        },
        {
          key: 'checkedIn',
          label: 'Checked in',
          sortable: true
        },
        {
          key: 'isAdmin',
          label: 'Is Admin',
          sortable: true
        }
      ],
      attendee: [],
      modalCallback: null,
      modalData: null,
      newAdminName: '',
      excelFile: null,
      importResult: {
        finished: false,
        total: 0,
        successCount: 0,
        failCount: 0,
        userCount: 0
      },
      importSocket: null
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
  destroyed () {
    this.closeSocket()
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
          this.toastError('Failed to assign admin')
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
            this.toastSuccess('Succeed to approve user ' + user)
          } else {
            this.attendee = this.attendee.filter(
              x => x.userInfo.id !== row.item.userInfo.id
            )
            this.toastSuccess('Succeed to reject user ' + user)
          }
        } catch (err) {
          if (answer) {
            this.toastError('Failed to approve user ' + user)
          } else {
            this.toastError('Failed to reject user ' + user)
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
        await this.syncImportProgress()
        try {
          await this.axios.post(`/api/event/${this.eventId}/import/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        } catch (err) {
          this.closeSocket()
          if (err.needHandle) {
            this.toastError('Failed to import! Please check your file conform to the template.')
          }
        }
      }
    },
    closeSocket () {
      if (this.importSocket) {
        this.importSocket.onclose = null
        this.importSocket.close()
        this.importSocket = null
      }
    },
    syncImportProgress () {
      this.importResult = {
        finished: false,
        total: 0,
        successCount: 0,
        failCount: 0,
        userCount: 0
      }
      let host = window.location.host
      // for dev
      if (host.search('localhost') !== -1) {
        host = 'localhost:8000'
      }
      this.closeSocket()
      this.importSocket = new WebSocket(`ws://${host}/ws/import/${this.eventId}/`)
      this.importSocket.onmessage = e => {
        const data = transformJSON2Object(JSON.parse(e.data))
        if (data.error) {
          this.toastError(data.error)
          this.closeSocket()
          return
        }
        this.importResult = data
        if (data.finished) {
          this.refresh()
        }
      }
      this.importSocket.onclose = e => {
        this.toastError('Failed to synchronize import progress')
        this.importSocket = null
      }
      return new Promise(resolve => {
        this.importSocket.onopen = e => {
          resolve()
        }
      })
    }
  }
}
</script>
