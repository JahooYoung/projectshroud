<template>
  <div />
</template>

<script>
export default {
  created () {
    if (this.user === null) {
      this.$router.push('/login')
      return
    }
    const token = this.$route.params.token
    this.axios.get(`/api/checkin/${token}/`)
      .then(res => this.axios.post(`/api/checkin/${token}/`))
      .then(res => alert('Checkin successfully'))
      .catch(err => err.response && alert(err.response.data.msg))
  }
}
</script>
