<template>
  <div>
    <sidebar-menu
      :menu="menu"
      width="200px"
      collapsed
      @collapse="x => collapsed = x"
    />
    <b-container
      id="admin-content"
      fluid
      :class="[{collapsed}]"
    >
      <transition
        name="fade"
        mode="out-in"
      >
        <router-view />
      </transition>
    </b-container>

    <b-modal
      id="modal-delete"
      title="Confirm Deletion"
      lazy
      @show="deleteInput = ''"
      @shown="$refs.deleteConfirmInput.focus()"
      @ok="deleteEvent"
    >
      <b-form @submit.prevent="deleteEvent">
        <b-form-input
          ref="deleteConfirmInput"
          v-model="deleteInput"
          :state="deleteInputState"
          :placeholder="`Enter '${confirmMessage}'`"
        />
        <b-form-text v-if="isLoading">
          Deleting... Hold on a minute please...
        </b-form-text>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import { SidebarMenu } from 'vue-sidebar-menu'
import Separator from './Separator.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCode, faInfo, faPlus, faUsers, faUserCog, faAngleLeft, faTasks, faArrowsAltH
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faCode, faInfo, faPlus, faUsers, faUserCog, faAngleLeft, faTasks, faArrowsAltH)

export default {
  name: 'EventAdminLayout',
  components: {
    SidebarMenu
  },
  data () {
    return {
      confirmMessage: 'I am sure',
      deleteInput: '',
      collapsed: true,
      menu: [
        {
          href: 'info',
          title: 'Basic Info',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'info'
            }
          }
        },
        {
          href: 'description',
          title: 'Description',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'code'
            }
          }
        },
        {
          href: 'administrator',
          title: 'Administrator',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'user-cog'
            }
          }
        },
        {
          href: 'attendee',
          title: 'Attendee',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'users'
            }
          }
        },
        {
          href: 'checkin',
          title: 'Checkin',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'tasks'
            }
          }
        },
        {
          header: true,
          component: Separator,
          visibleOnCollapse: true
        },
        {
          href: `/event/${this.$route.params.id}`,
          title: 'Back',
          icon: {
            element: FontAwesomeIcon,
            attributes: {
              icon: 'angle-left'
            }
          }
        }
      ]
    }
  },
  computed: {
    deleteInputState () {
      return this.deleteInput === this.confirmMessage
    }
  },
  methods: {
    async deleteEvent () {
      if (!this.deleteInputState) {
        return
      }
      await this.axios.delete(`/api/event/${this.$route.params.id}/`)
      this.toastSuccess('Successfully delete event')
      this.$router.push('/admin-event')
    }
  }
}
</script>

<style lang="scss">
$primaryColor: #2196F3;
$baseBg: #3d3d3d;

@import "vue-sidebar-menu/src/scss/vue-sidebar-menu.scss";

#admin-content {
  padding-left: 210px;
  transition: 0.3s padding-left;
}

#admin-content.collapsed {
  padding-left: 60px;
  transition: 0.3s padding-left;
}

.v-sidebar-menu {
  margin-top: 4rem;
  height: calc(100vh - 4rem);
}

.v-sidebar-menu .vsm-icon {
  padding: 0.3rem;
}
</style>
