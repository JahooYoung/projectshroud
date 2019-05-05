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
        {{ $t('Website name') }}
      </b-navbar-brand>

      <b-navbar-toggle target="nav_collapse" />

      <b-collapse
        id="nav_collapse"
        is-nav
      >
        <b-navbar-nav>
          <b-nav-item to="/">
            {{ $t('Home') }}
          </b-nav-item>
          <b-nav-item to="/event">
            {{ $t('Event') }}
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <SearchBox />

          <b-nav-item-dropdown
            :text="$t('Language')"
            right
          >
            <b-dropdown-item
              :active="$i18n.locale === 'en'"
              @click="changeLocale('en')"
            >
              English
            </b-dropdown-item>
            <b-dropdown-item
              :active="$i18n.locale === 'zh'"
              @click="changeLocale('zh')"
            >
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
                {{ $t('Notification') }}
                <b-badge variant="dark">
                  1
                </b-badge>
              </b-dropdown-item>
              <b-dropdown-divider />
              <b-dropdown-item
                to="/user-profile"
                exact-active-class=""
              >
                {{ $t('Your Profile') }}
              </b-dropdown-item>
              <b-dropdown-item
                to="/registered-event"
                exact-active-class=""
              >
                {{ $t('Registered events') }}
              </b-dropdown-item>
              <b-dropdown-item
                to="/admin-event"
                exact-active-class=""
              >
                {{ $t('Admin events') }}
              </b-dropdown-item>
              <b-dropdown-divider />
              <b-dropdown-item @click="logout">
                {{ $t('Logout') }}
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </div>
          <div v-else>
            <b-nav-item to="/login">
              {{ $t('Login') }}
            </b-nav-item>
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import SearchBoxLoading from './SearchBoxLoading.vue'
import { loadLanguageAsync } from '@/i18n'

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
    },
    changeLocale (lang) {
      loadLanguageAsync(lang)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-div {
  margin-bottom: 5rem
}

/* #nav_collapse .router-link-exact-active {
  color: #ffffff;
} */
</style>
