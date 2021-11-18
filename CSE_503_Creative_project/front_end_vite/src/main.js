import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import mitt from 'mitt'

// refer to https://juejin.cn/post/6945369322206265380
const app = createApp(App)
app.config.globalProperties.$bus = new mitt()
app.mount('#app')