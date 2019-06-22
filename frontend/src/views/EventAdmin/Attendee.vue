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

          <template #checkedIn="row">
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

          <template #isAdmin="row">
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
            <!-- <font-awesome-icon
              v-if="!row.value"
              :id="'checkin-popover-' + row.item.userInfo.id"
              icon="plus"
              :style="{ color: '#2196F3' }"
              class="ml-3"
              @click="assignAdmin(row.item)"
            /> -->
          </template>

          <template #actions="row">
            <b-button
              size="sm"
              @click="row.toggleDetails"
            >
              {{ row.detailsShowing ? $t('Hide Details') : $t('Show Details') }}
            </b-button>
          </template>

          <template #row-details="row">
            <b-card-group deck>
              <b-card>
                <template #header>
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mt-1">
                      {{ $t('User Information') }}
                    </h6>
                    <b-button
                      variant="primary"
                      size="sm"
                      :disabled="row.item.isAdmin"
                      @click="assignAdmin(row.item)"
                    >
                      {{ $t('Assign Admin') }}
                    </b-button>
                  </div>
                </template>
                <b-card-text>
                  <strong>{{ $t('Real name:') }}</strong> {{ row.item.userInfo.realName }} <br>
                  <strong>{{ $t('Mobile:') }}</strong> {{ row.item.userInfo.mobile }} <br>
                  <strong>{{ $t('Email:') }}</strong> {{ row.item.userInfo.email }} <br>
                </b-card-text>
              </b-card>
              <b-card>
                <template #header>
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mt-1">
                      {{ $t('Transport') }} &amp; {{ $t('Accommodation') }}
                    </h6>
                    <b-button
                      variant="success"
                      size="sm"
                      @click="editTransport(row)"
                    >
                      {{ $t('Edit') }}
                    </b-button>
                  </div>
                </template>
                <b-card-text v-if="row.item.transportInfo">
                  <strong>{{ row.item.transportInfo.transportType }}</strong> {{ row.item.transportInfo.transportId }} <br>
                  <strong>{{ $t('From') }}</strong> {{ row.item.transportInfo.departStation }} <br>
                  {{ row.item.transportInfo.departTime.toLocaleString() }} <br>
                  <strong>{{ $t('To') }}</strong> {{ row.item.transportInfo.arrivalStation }} <br>
                  {{ row.item.transportInfo.arrivalTime.toLocaleString() }}
                  <div v-if="row.item.transportInfo.accommodation">
                    <strong>{{ $t('Stay at') }} </strong> {{ row.item.transportInfo.accommodation }}
                  </div>
                  <div v-if="row.item.transportInfo.otherDetail">
                    <strong>{{ $t('p.s.') }}</strong> {{ row.item.transportInfo.otherDetail }}
                  </div>
                </b-card-text>
                <b-card-text v-else>
                  {{ $t('None') }}
                </b-card-text>
              </b-card>
            </b-card-group>
          </template>
        </b-table>
      </template>
    </TableLayout>

    <b-modal
      ref="modal-approve"
      cancel-variant="danger"
      :ok-title="$t('Accept')"
      :cancel-title="$t('Reject')"
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
      :ok-title="$t('OK')"
      :cancel-title="$t('Cancel')"
      @ok="modalCallback && modalCallback(true)"
      @cancel="modalCallback && modalCallback(false)"
      @hide="modalCallback && modalCallback(null)"
    >
      <p class="my-3">
        {{ $t('Are you sure to add') + newAdminName + $t('as an administrator?') }} <br>
        <b>{{ $t('Warning:') }}</b> {{ $t('You cannot undo this operation!') }}
      </p>
    </b-modal>

    <input
      id="file-input"
      type="file"
      accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      style="display: none"
    >

    <transport-modal ref="tp-modal" />
  </b-container>
</template>

<script>
import {
  BProgress, BProgressBar, BAlert, BDropdown, BDropdownItem, BButton, BTable,
  BCardGroup, BCard, BCardText
} from 'bootstrap-vue'
import TableLayout from '@/components/TableLayout.vue'
import TransportModal from '@/components/TransportModal.vue'
import { transformJSON2Object } from '@/plugins/axios.js'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTimes, faCheck, faPlus)

export default {
  name: 'EventAdminAttendee',
  components: {
    TableLayout,
    TransportModal,
    FontAwesomeIcon,
    BProgress,
    BProgressBar,
    BAlert,
    BDropdown,
    BDropdownItem,
    BButton,
    BTable,
    BCardGroup,
    BCard,
    BCardText
  },
  data () {
    return {
      attendee: [],
      modalCallback: null,
      modalData: null,
      newAdminName: '',
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
    },
    fields () {
      return [
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
  destroyed () {
    this.closeSocket()
  },
  methods: {
    async refresh () {
      const res = await this.axios.get(`/api/event/${this.eventId}/attendee/`)
      this.attendee = res.data
    },
    editTransport (row) {
      const item = this.attendee[row.index]
      this.$refs['tp-modal'].resetShow(item.transportInfo, item.eventInfo.id)
        .then(transport => {
          if (transport !== false) {
            item.transportInfo = transport
          }
        })
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
    chooseFiles () {
      const input = document.getElementById('file-input')
      input.click()
      return new Promise(resolve => {
        input.onchange = ev => {
          input.onchange = null
          const files = input.files
          input.files = null
          resolve(files)
        }
      })
    },
    async importExcel () {
      const files = await this.chooseFiles()
      if (files.length > 0) {
        const formData = new FormData()
        formData.append('file', files[0])
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
            this.toastError(this.$t('Failed to import! Please check your file conform to the template.'))
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
      this.closeSocket()
      this.importResult = {
        finished: false,
        total: 0,
        successCount: 0,
        failCount: 0,
        userCount: 0
      }
      let host = window.location.host; let protocol = window.location.protocol
      // for dev
      if (host.search('localhost') !== -1) {
        host = 'localhost:8000'
      }
      protocol = protocol === 'https:' ? 'wss:' : 'ws:'
      this.importSocket = new WebSocket(`${protocol}//${host}/ws/import/${this.eventId}/`)
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
