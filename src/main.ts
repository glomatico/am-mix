import "@mdi/font/css/materialdesignicons.css";
import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "vuetify/styles";
import App from "./App.vue";
import enMessages from "./locales/en.json";
import { router } from "./router";

const i18n = createI18n({
  fallbackLocale: "en",
  messages: {
    en: enMessages,
  },
});

const vuetify = createVuetify({
  components,
  directives,
});

createApp(App).use(i18n).use(router).use(vuetify).mount("#app");
