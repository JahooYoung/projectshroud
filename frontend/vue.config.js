module.exports = {
  lintOnSave: true,

  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000'
        // pathRewrite: { '^/api': '' }
      }
    }
  },

  // publicPath: undefined,
  // outputDir: undefined,
  // runtimeCompiler: undefined,
  // productionSourceMap: undefined,
  // parallel: undefined,
  // css: undefined,
  assetsDir: 'static',

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
}
