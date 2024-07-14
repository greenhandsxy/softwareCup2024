import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Elementplus from 'element-plus'
import 'element-plus/dist/index.css'
import elementIcon from "./plugins/icons";
import VueLatex from 'vatex'


const app = createApp(App)
    app
    .use(store)
    .use(Elementplus)
    .use(router)
    .use(elementIcon)
    .use(VueLatex)
// app.config.globalProperties.$store = store; // 注入store
    app.mount('#app')
