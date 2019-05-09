<template>
  <MavonEditor
    v-model="description"
    class="md-editor"
    :ishljs="false"
    :external-link.camel="false"
    placeholder="Loading..."
    @change="change"
    @save="save"
  />
</template>

<script>
import { mavonEditor } from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import 'mavon-editor/dist/markdown/github-markdown.min.css'

export default {
  name: 'EventAdminDescription',
  components: {
    MavonEditor: mavonEditor
  },
  data () {
    return {
      description: '',
      savedDescription: '',
      saved: true
    }
  },
  created () {
    this.axios.get(`/api/event/${this.$route.params.id}/`)
      .then(res => {
        this.description = this.savedDescription = res.data.description
        if (this.description === '') {
          this.description = `# ${res.data.title}\nGive your description here...`
        }
      })
  },
  beforeRouteLeave (to, from, next) {
    if (this.saved || this.description === this.savedDescription) {
      next()
    } else {
      this.$bvModal.msgBoxConfirm('Do you want to save the description?', {
        title: 'Not saved yet',
        centered: true
      })
        .then(ans => {
          if (ans === true) {
            this.save()
              .then(() => next())
          } else if (ans === false) {
            next()
          }
        })
    }
  },
  methods: {
    change () {
      this.saved = false
    },
    save (value, html) {
      return this.axios.patch(`/api/event/${this.$route.params.id}/`, {
        description: value,
        description_html: html
      })
        .then(res => {
          this.saved = true
          this.savedDescription = res.data.description
          this.$bvToast.toast('Description saved successfully', {
            title: `Success`,
            autoHideDelay: 1000,
            solid: true
          })
        })
    }
  }
}
</script>

<style scoped>
.md-editor {
  min-height: calc(100vh - 6rem);
  max-height: calc(100vh - 6rem);
  z-index: 20;
}
</style>

<style>
.auto-textarea-input, .auto-textarea-input:focus {
  box-shadow: none;
}
</style>
