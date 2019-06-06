module.exports = {
  devServer: {
    // Server: 'http://10.128.202.42:8000'
    // LocalServer: 'http://localhost:8000'
    proxy: {
      '^/api/': {
        target: 'http://10.128.202.42:8000'
      },
      '^/admin/': {
        target: 'http://10.128.202.42:8000'
      },
      '^/static/rest_framework/': {
        target: 'http://10.128.202.42:8000'
      }
    }
  },

  chainWebpack: config => {
    config
      .plugin('html')
      .tap(options => {
        if (options[0].minify) {
          options[0].minify.minifyCSS = true
        }
        return options
      })

    // config.module
    //   .rule('gzip')
    //   .test(/\.gz$/)
    //   .use('gzip-loader')
    //   .loader('gzip-loader')
    //   .end()

    // config.module
    //   .rule('txt')
    //   .test(/\.txt$/)
    //   .use('@/loaders/txtLoader')
    //   .loader('@/loaders/txtLoader')
    //   .end()
  },

  productionSourceMap: false,
  assetsDir: 'static'
}
