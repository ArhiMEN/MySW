const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    devServer: {
      host: '0.0.0.0',
      port: 8000,
      https: false,
      proxy: {
        '^/api': {
          target: 'http://0.0.0.0:8001/',
          changeOrigin: true
        }
      }
    }
  }
})
