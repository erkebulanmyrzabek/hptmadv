import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

//TODO: Еркебулан надо добавить Telegram SDK
// import TelegramWebApp from '@twa-dev/sdk';
// TelegramWebApp.ready();

const app = createApp(App);
const pinia = createPinia();
app.use(router);
app.use(pinia);

app.mount('#app');