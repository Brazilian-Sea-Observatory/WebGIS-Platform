import Vue from 'vue';
import VueI18n from 'vue-i18n';

import pt from './locale/pt-br';
import fr from './locale/fr';
import en from './locale/en';
Vue.use(VueI18n);

export const i18n = new VueI18n({
    messages: { pt, fr, en },
    locale: 'pt',
});
