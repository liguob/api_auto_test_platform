import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from "axios"
import echarts from 'echarts'
import CodeEditor from "bin-code-editor/src/components/code-editor";
import 'bin-code-editor/lib/styles/index.css'

Vue.prototype.http = axios
Vue.use(CodeEditor)
Vue.use(ElementUI)
Vue.prototype.$echarts = echarts
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
// Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
