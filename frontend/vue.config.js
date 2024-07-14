const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    // devServer: {
    //   proxy: {
    //     '/api': {
    //       target: 'http://localhost:8888',
    //       changeOrigin: true,
    //       rewrite: (path) => path.replace(/^\/api/, ""),
    //     }
    //   }
    // }
})
// module.exports = defineConfig(
//     {
//         // ...
//         transpileDependencies: true,
//         configureWebpack: {
//             module: {
//                 rules: [
//                     // ...
//                     {
//                         test: /\.vue/,
//                         loader: 'vue-loader'
//                     },
//                     {
//                         test: /\.tsx?/,
//                         loader: 'ts-loader',
//                         exclude: /node_modules/,
//                         options: {
//                             appendTsSuffixTo: [/\.vue$/]
//                         }
//                     },
//                     // ...
//                 ]
//             },
//             resolve: {
//                 extensions: ['.ts', '.js', '.vue', '.json']
//             },
//             // ...
//         }
//     }
// )
