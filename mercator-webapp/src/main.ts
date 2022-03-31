import '@babel/polyfill';
import Vue from 'vue';
import './plugins/vuetify';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';
import Vuetify from 'vuetify';
import { i18n } from './i18n';

Vue.config.productionTip = false;
// if (window.location.protocol === 'http:') window.location.href = `https://${window.location.host}`;
new Vue({
  router,
  store,
  i18n,
  render: (h) => h(App),
}).$mount('#app');
