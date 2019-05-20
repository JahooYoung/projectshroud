<template>
  <div>
    <input
      :id="inputId"
      v-model="query"
      class="form-control"
      :placeholder="placeholder"
      :required="required"
    >
    <custom-map-searchbox
      :input="inputId"
      :type="type"
      @select="selectSearch"
    />
  </div>
</template>

<script>
import VueAMap, { createCustomComponent } from 'vue-amap'

VueAMap.initAMapApiLoader({
  key: '854afe95f36103ef9a12fbc665ae509d',
  plugin: ['AMap.Autocomplete'],
  // plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  // 默认高德 sdk 版本为 1.4.4
  v: '1.4.4'
})

const customMapSearchbox = createCustomComponent({
  props: {
    input: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'Other'
    }
  },
  init (options, map) {
  //   return new Promise(resolve => {
  //     AMap.plugin(['AMap.Autocomplete','AMap.PlaceSearch'], () => {
  //       const autocomplete = new AMap.Autocomplete(options)
  //       AMap.event.addListener(autocomplete, 'select', (e) => {
  //         this.$emit('select', e.poi)
  //       });
  //       resolve(autocomplete)
  //     })
  //   })
  },
  computed: {
    poiType () {
      switch (this.type) {
        case 'Flight':
          return '150104'
        case 'Train':
          return '150200'
        default:
          return ''
      }
    }
  },
  watch: {
    poiType () {
      this.$amapComponent.setType(this.poiType)
    }
  },
  contextReady (_options) {
    const options = {
      ..._options,
      input: this.input,
      type: this.poiType
    }
    AMap.plugin(['AMap.Autocomplete'], () => {
      const autocomplete = new AMap.Autocomplete(options)
      AMap.event.addListener(autocomplete, 'select', (e) => {
        this.$emit('select', e.poi)
      })
      this.$amapComponent = autocomplete
    })
  }
})

export default {
  name: 'LocationInput',
  components: {
    customMapSearchbox
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'Other'
    },
    placeholder: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      inputId: 'map-searchbox-input-' + Math.random(),
      query: this.value
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
  methods: {
    selectSearch (poi) {
      // console.log(poi)
      this.query = poi.name
      // this.query = poi.district + poi.name
    }
  }
}
</script>

<style>
.amap-sug-result {
  z-index: 2048;
}
</style>
