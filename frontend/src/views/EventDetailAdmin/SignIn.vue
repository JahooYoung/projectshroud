<template>
  <div>
    <b-button
      size="lg"
      :variant="signing ? 'danger' : 'primary'"
      @click="onClick"
    >
      {{ signing ? 'Stop' : 'Start'}} Sign In
    </b-button>
    <b-img
      v-if="signing"
      center
      style="margin-top: 10px"
      height="500px"
      src="https://picsum.photos/125/125/?image=58"
      alt="Center image"
    ></b-img>
  </div>
</template>

<script>
export default {
  data () {
    return {
      signing: false
    }
  },
  methods: {
    onClick () {
      if (this.signing) {
        this.signing = false
      } else {
        this.signing = true
      }
    }
  }
}
</script>
