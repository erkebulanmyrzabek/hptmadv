import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';


import { VueTelegramPlugin } from 'vue-tg'



const app = createApp(App);
const pinia = createPinia();
app.use(VueTelegramPlugin)
app.use(router);
app.use(pinia);

app.mount('#app');