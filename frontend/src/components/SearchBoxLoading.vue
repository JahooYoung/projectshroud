<template>
  <b-nav-form>
    <div
      class="input-group mr-sm-2"
      style="width: 20em"
    >
      <input
        class="form-control form-control-sm type-ahead-select taller"
        :placeholder="$t('Preparing search...')"
        disabled
      >
    </div>
  </b-nav-form>
</template>

<script>
export default {
  name: 'SearchBoxLoading'
}
</script>

<style scoped>
div.input-group input.form-control.type-ahead-select {
  border-top-right-radius: .25rem;
  border-bottom-right-radius: .25rem;
}
</style>
