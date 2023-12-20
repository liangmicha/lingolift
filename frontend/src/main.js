import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // This assumes the file is named index.js
import './assets/main.css'; // Importing global stylesheet

createApp(App).use(router).mount('#app');
