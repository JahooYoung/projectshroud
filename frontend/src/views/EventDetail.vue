<template>
  <div>
    <EventDetailAdmin v-if="isAdmin"/>
    <div v-if="!isAdmin">
      <!-- fill this in -->
      zld tql
    </div>
  </div>
</template>

<script>
import EventDetailAdmin from './EventDetailAdmin'

export default {
  data () {
    return {
      isAdmin: false
    }
  },
  components: {
    EventDetailAdmin
  }
}
</script>
