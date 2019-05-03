<template>
  <div class="navbar-div">
    <b-navbar
      id="nav"
      fixed="top"
      toggleable="md"
      type="dark"
      variant="dark"
    >
      <b-navbar-brand to="/">
        NavBar
      </b-navbar-brand>

      <b-navbar-toggle target="nav_collapse" />

      <b-collapse
        id="nav_collapse"
        is-nav
      >
        <b-navbar-nav>
          <b-nav-item to="/">
            Home
          </b-nav-item>
          <b-nav-item to="/event">
            Event
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <!-- <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search" />
            <b-button size="sm" class="my-2 my-sm-0">Search</b-button>
          </b-nav-form> -->

          <SearchBox />

          <b-nav-item-dropdown
            text="Lang"
            right
          >
            <b-dropdown-item href="#">
              English
            </b-dropdown-item>
            <b-dropdown-item href="#">
              简体中文
            </b-dropdown-item>
          </b-nav-item-dropdown>

          <div v-if="user !== null">
            <b-nav-item-dropdown right>
              <template slot="button-content">
                {{ user }}
                <b-badge variant="light">
                  1
                </b-badge>
              </template>
              <b-dropdown-item
                href="#"
                exact-active-class=""
              >
                Notification
                <b-badge variant="dark">
                  1
                </b-badge>
              </b-dropdown-item>
              <b-dropdown-divider />
              <b-dropdown-item
                to="/user-profile"
                exact-active-class=""
              >
                Your Profile
              </b-dropdown-item>
              <b-dropdown-item
                to="/registered-event"
                exact-active-class=""
              >
                Registered events
              </b-dropdown-item>
              <b-dropdown-item
                to="/admin-event"
                exact-active-class=""
              >
                Admin events
              </b-dropdown-item>
              <b-dropdown-divider />
              <b-dropdown-item @click="logout">
                Logout
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </div>
          <div v-else>
            <b-nav-item to="/login">
              Login
            </b-nav-item>
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import SearchBoxLoading from './SearchBoxLoading.vue'

export default {
  name: 'NavBar',
  components: {
    SearchBox: () => ({
      component: import('./SearchBox.vue'),
      loading: SearchBoxLoading
    })
  },
  methods: {
    logout () {
      this.axios.post('/api/auth/logout/')
        .then(res => {
          this.$store.commit('setUserState', null)
          this.$router.push('/')
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-div {
  margin-bottom: 4em
}

#nav_collapse .router-link-exact-active {
  color: #ffffff;
}
</style>
