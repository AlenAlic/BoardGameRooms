// Main components
import Vue from "vue";
import App from "./App";

// Main extension
import router from "./router";
import store from "./store";
import i18n from "./languages";
import vuetify from "./plugins/Vuetify";

// Modules
import UtilitiesHandler from "./assets/js/utilities";
import VueSocketIOExt from "vue-socket.io-extended";
import io from "socket.io-client";

// Register the config independent modules.
Vue.use(UtilitiesHandler);
const backend = process.env.NODE_ENV === "production" ? `//${window.location.host}` : "http://127.0.0.1:5000";
Vue.use(VueSocketIOExt, io(backend));

// Turn off Vue Production tip
Vue.config.productionTip = false;

// Mount App
new Vue({
  router,
  store,
  i18n,
  vuetify,
  render: h => h(App)
}).$mount("#app");
