const { defineConfig } = require('@vue/cli-service')

module.exports = {
  devServer: {
    host: '0.0.0.0',
    hot: true,
    allowedHosts: 'all',
    watchFiles: '**/*',
  },
};