import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import mitt from 'mitt'

const app = createApp(App)
app.config.globalProperties.$bus = new mitt()
app.mount('#app')