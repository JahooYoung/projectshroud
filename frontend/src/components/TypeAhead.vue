<template>
  <div
    class="input-group"
    :class="[classes]"
  >
    <input
      ref="input"
      v-model="query"
      type="text"
      autocomplete="off"
      class="form-control type-ahead-select taller"
      :placeholder="placeholder"
      @keydown.down.prevent="down"
      @keydown.up.prevent="up"
      @keydown.enter.prevent="hit"
      @keydown.esc.prevent="blur"
      @focus="focus = true"
      @blur="focus = false"
      @input="update($event)"
    >

    <ul
      v-if="focus && !isEmpty"
      class="dropdown-menu-list dropdown-menu"
      role="menu"
      aria-labelledby="dropdownMenu"
    >
      <li>
        {{ $t('Search results for',[query]) }}:
        <hr class="mt-1 mb-0">
      </li>
      <li
        v-for="(item, index) in items"
        :key="'li' + index"
        @mousedown="hit"
        @mousemove="setActive(index)"
      >
        <div
          class="py-2"
          :class="{active:activeClass(index)}"
        >
          <a v-html="highlighting(item, vue)" />
        </div>
        <hr class="my-0">
      </li>
      <li
        v-show="!hasItems"
        class="py-2"
      >
        <a>
          <span
            v-if="!loading"
            v-html="noResultText"
          />
          <span
            v-else
            v-html="searchingText"
          />
        </a>
        <hr class="my-1">
      </li>
      <li align="right">
        <ais-powered-by />
      </li>
    </ul>
  </div>
</template>

<script>
import { AisPoweredBy } from 'vue-instantsearch'

function escapeRegExp (str) {
  // eslint-disable-next-line
  return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, '\\$&')
}

export default {
  name: 'TypeAhead',
  components: {
    AisPoweredBy
  },
  props: {
    selectFirst: {
      // 是否选择第一个选项
      required: false,
      type: Boolean,
      default: false
    },
    limit: {
      // 最大显示量
      required: false,
      type: Number,
      default: 10
    },
    delayTime: {
      // 发送延迟时间
      required: false,
      default: 500,
      type: Number
    },
    placeholder: {
      // 是否有placeholder
      required: false,
      type: String,
      default: ''
    },
    noResultText: {
      // 如果显示搜索状态，无结果的文本
      required: false,
      type: String,
      default: 'No result'
    },
    searchingText: {
      // 如果显示搜索状态，搜索的文本
      required: false,
      type: String,
      default: 'Searching...'
    },
    classes: {
      // 所给填写框增加的类
      required: false,
      type: String,
      default: ''
    },
    value: {
      required: false,
      type: String,
      default: ''
    },
    onHit: {
      required: false,
      type: Function,
      default: function (item) {
        this.query = item
      }
    },
    highlighting: {
      // 高亮结果
      required: false,
      type: Function,
      default: function (item) {
        var re = new RegExp(escapeRegExp(this.query), 'ig')
        var matches = item.match(re)
        matches && matches.forEach(match => {
          item = item.replace(match, `<b>${match}</b>`)
        })
        return item
      }
    },
    render: {
      // 对结果进行处理
      required: false,
      type: Function,
      default: function (items) {
        return items
      }
    },
    getResponse: {
      // 如何处理得到的请求
      required: true,
      type: Function
    },
    fetch: {
      // 如何获取数据
      required: true,
      type: Function
    },
    objectArray: {
      required: false,
      type: Array,
      default: null
    }
  },
  data () {
    return {
      items: [],
      query: '',
      current: -1,
      focus: false,
      loading: false,
      lastTime: 0,
      data: []
    }
  },
  computed: {
    vue () {
      return this
    },
    hasItems () {
      return this.items.length > 0
    },
    isEmpty () {
      return this.query === ''
    }
  },
  watch: {
    value: function (value) {
      this.query = this.query !== value ? value : this.query
    },
    query: function (value) {
      this.$emit('input', value)
    }
  },
  mounted () {
    this.query = this.value
    /***
     * 使得其点击之外的部分自动收起
     */
    // document.addEventListener('click', (e) => {
    //   if (!this.$el.contains(e.target)) {
    //     this.reset()
    //   }
    // })
    if (this.objectArray) {
      this.objectArray.sort()
    }
  },
  methods: {
    objectUpdate () {
      var filtered = this.objectArray.filter(entity => entity.toLowerCase().includes(this.query.toLowerCase()))
      this.data = this.limit ? filtered.slice(0, this.limit) : filtered
      this.items = this.render(this.limit ? this.data.slice(0, this.limit) : this.data, this)

      this.current = -1
      if (this.selectFirst) {
        this.down()
      }
    },
    update (event) {
      this.lastTime = event.timeStamp
      if (!this.query) {
        return
      }
      // 添加的延时
      setTimeout(() => {
        if (this.lastTime - event.timeStamp === 0) {
          if (this.objectArray) {
            return this.objectUpdate()
          }
          this.items = []
          this.loading = true
          this.fetch().then((response) => {
            if (this.query) {
              let data = this.getResponse(response)
              this.data = this.limit ? data.slice(0, this.limit) : data
              this.items = this.render(this.limit ? data.slice(0, this.limit) : data, this)
              this.current = -1
              this.loading = false
              if (this.selectFirst) {
                this.down()
              }
            }
          })
        }
      }, this.delayTime)
    },
    setActive (index) {
      this.current = index
    },
    activeClass (index) {
      return this.current === index
    },
    hit () {
      if (this.current !== -1) {
        this.onHit(this.items[this.current], this, this.current)
      }
      this.blur()
    },
    up () {
      if (this.current > 0) {
        this.current--
      } else if (this.current === -1) {
        this.current = this.items.length - 1
      } else {
        this.current = -1
      }
      if (!this.selectFirst && this.current !== -1) {
        this.onHit(this.items[this.current], this)
      }
    },
    down () {
      if (this.current < this.items.length - 1) {
        this.current++
      } else {
        this.current = -1
      }
      if (!this.selectFirst && this.current !== -1) {
        this.onHit(this.items[this.current], this)
      }
    },
    blur () {
      this.$refs.input.blur()
    }
  }
}
</script>

<style scoped>
/* div.input-group input.form-control.type-ahead-select {
  background: #fff url(../assets/search.png) 5px 5px no-repeat;
  background-size: 20px;
  border-radius: .25rem;
  padding-left: 28px;
  border-top-right-radius: .25rem;
  border-bottom-right-radius: .25rem;
} */
.dropdown-menu-list {
  display: list-item;
  width: 100%;
}
ul li {
  padding: 0px .25rem;
  margin: 0px .25rem;
  cursor: pointer;
  border-radius: 4px;
}
ul li div {
  border-radius: 4px;
}
ul li div.active {
  background-color: #e4e4e4d0;
}
</style>
