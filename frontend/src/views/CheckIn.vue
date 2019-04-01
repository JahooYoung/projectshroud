<template>
  <div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    user: 'user'
  }),
  mounted () {
    if (this.user === null) {
      this.$router.push('/login')
    } else {
      this.axios.get(`/api/checkin/${this.$route.params.token}`)
        .then(res => {
          console.log(res)
          if (res.status === 200) {
            alert('checkin success!')
          } else {
            alert('checkin failed!')
          }
        })
    }
  }
}
</script>
