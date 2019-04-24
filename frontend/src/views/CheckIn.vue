<template>
  <div />
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
      this.axios.get(`/api/checkin/${this.$route.params.token}/`)
        .then(res => {
          console.log(res)
          if (res.status === 200) {
            this.axios.post(`/api/checkin/${this.$route.params.token}/`)
              .then(res => {
                if (res.status === 202) {
                  alert('checkin success!')
                } else {
                  alert(res.data.msg)
                }
              })
          } else {
            alert(res.data.msg)
          }
        })
    }
  }
}
</script>
