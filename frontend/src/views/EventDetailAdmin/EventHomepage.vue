<template>
  <div id="editor">
    <textarea id="editor-left" @scroll="onScroll" v-model="input"></textarea>
    <section class="preview">
      <vue-markdown id="editor-right" :source="input"></vue-markdown>
    </section>
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'
// import lodash from 'lodash'

export default {
  data () {
    return {
      input: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.replace(/a/g, '# hello\n')
    }
  },
  components: {
    VueMarkdown
  },
  methods: {
    // update: lodash.debounce(function (e) {
    //   this.input = e.target.value
    // }, 300),
    onScroll () {
      const editorLeft = document.querySelector('#editor-left')
      const editorRight = document.querySelector('#editor-right')
      const editorLeftTotal = editorLeft.scrollHeight - editorLeft.clientHeight
      const editorRightTotal = editorRight.scrollHeight - editorRight.clientHeight
      editorRight.scrollTop = editorLeft.scrollTop / editorLeftTotal * editorRightTotal
    }
  }
}
</script>

<style scope>
#editor {
  margin: 0;
  height: calc(100vh - 5em);
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  text-align: left;
}

#editor textarea, .preview {
  display: inline-block;
  width: 49%;
  height: calc(100vh - 5em);
  vertical-align: top;
  box-sizing: border-box;
  padding: 0 20px;
}

#editor textarea {
  border: none;
  border-right: 1px solid #ccc;
  resize: none;
  outline: none;
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: 'Monaco', courier, monospace;
  padding: 20px;
}

#editor #editor-right {
  height: 100%;
  overflow: auto;
  border: 1px solid#ccc;
  border-radius: 4px;
}

#editor code {
  color: #f66;
}
</style>
