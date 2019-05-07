module.exports = {
  lintOnSave: true,

  devServer: {
    proxy: {
      '/api/': {
        target: 'http://localhost:8000'
      },
      '/admin/': {
        target: 'http://localhost:8000'
      },
      '/static/rest_framework/': {
        target: 'http://localhost:8000'
      }
    }
  },

  chainWebpack: config => {
    config.plugin('html').tap(options => {
      if (options[0].minify) {
        options[0].minify.minifyCSS = true
      }
      return options
    })
  },

  productionSourceMap: false,
  assetsDir: 'static'
}
