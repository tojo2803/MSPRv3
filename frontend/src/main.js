import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import i18n from './i18n'
import './assets/main.css';
import { createPinia } from 'pinia';

const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(router);
app.use(createPinia());
app.use(i18n);
app.mount('#app');