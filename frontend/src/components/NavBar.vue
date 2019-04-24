<template>
  <div class="navbar-div">
    <b-navbar
      fixed="top"
      toggleable="md"
      type="dark"
      variant="info"
      id="nav"
    >
      <b-navbar-brand to="/">
        NavBar
      </b-navbar-brand>

      <b-navbar-toggle target="nav_collapse" />

      <b-collapse
        is-nav
        id="nav_collapse"
      >
        <b-navbar-nav>
          <b-nav-item to="/">
            Home
          </b-nav-item>
          <b-nav-item to="/event">
            Event
          </b-nav-item>
          <!-- <b-nav-item to="#" disabled>Disabled</b-nav-item> -->
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
              EN
            </b-dropdown-item>
            <b-dropdown-item href="#">
              ES
            </b-dropdown-item>
            <b-dropdown-item href="#">
              RU
            </b-dropdown-item>
            <b-dropdown-item href="#">
              FA
            </b-dropdown-item>
          </b-nav-item-dropdown>

          <div v-if="user != null">
            <b-nav-item-dropdown right>
              <template slot="button-content">
                {{ user }}
              </template>
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
              <b-dropdown-item @click="logout()">
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
import { mapState } from 'vuex'
import SearchBox from './SearchBox'

export default {
  name: 'NavBar',
  components: {
    SearchBox
  },
  computed: mapState({
    user: 'user'
  }),
  methods: {
    logout () {
      const commit = this.$store.commit
      const router = this.$router
      this.axios.post('/api/auth/logout/')
        .then(res => {
          commit('setUserState', null)
          router.push('/')
        })
        .catch(err => {
          alert('fail to logout!')
          console.log(err)
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
