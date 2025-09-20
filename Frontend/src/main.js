import { createApp } from 'vue'
import { RouterView } from 'vue-router';
import App from './App.vue'
import router from './router'
import './assets/theme.css'

const app = createApp(App)

app.use(router)
app.component('router-view', RouterView);

app.mount('#app')
