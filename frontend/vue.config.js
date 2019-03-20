module.exports = {
  lintOnSave: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        pathRewrite: {'^/api' : ''}
      }
    }
  },
  assetsDir: 'static',
  // publicPath: undefined,
  // outputDir: undefined,
  // runtimeCompiler: undefined,
  // productionSourceMap: undefined,
  // parallel: undefined,
  // css: undefined,
}
