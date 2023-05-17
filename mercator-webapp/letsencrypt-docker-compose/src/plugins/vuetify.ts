import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

import pt from '../locale/pt-br';
import fr from '../locale/fr';
import en from '../locale/en';

Vue.use(Vuetify, {
  theme: {
    primary: '#4e76ed',
    secondary: '#424242',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
  },
  lang: {
    locales: { pt, fr, en },
  },
  customProperties: true,
  iconfont: 'md',
});
