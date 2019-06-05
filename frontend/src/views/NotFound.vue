<template>
  <div>
    <h3 class="align-center pb-3 display-4">
      404 NOT FOUND
    </h3>
    <h4 class="align-center display-5">
      迷路了:-(<br>
      点
      <b-link to="/">
        这里
      </b-link>
      返回主页
    </h4>
  </div>
</template>

<script>
import { BLink } from 'bootstrap-vue'

export default {
  name: 'NotFound',
  components: {
    BLink
  }
}
</script>
