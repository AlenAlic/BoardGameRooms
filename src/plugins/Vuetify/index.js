import Vue from "vue";
import Vuetify from "vuetify/lib";
import "vuetify/dist/vuetify.min.css";
import "@mdi/font/css/materialdesignicons.css";
import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

const opts = {
  theme: {
    themes: {
      light: {
        primary: colors.blue.darken2,
        secondary: colors.grey.darken3,
        accent: colors.blue.accent1,
        error: colors.red.accent2,
        info: colors.blue,
        success: colors.green,
        warning: colors.amber
      },
      dark: {
        primary: colors.blue.darken4,
        secondary: colors.grey.darken2,
        accent: colors.cyan.darken2,
        error: colors.red.darken2,
        info: colors.blue.darken2,
        success: colors.green.darken2,
        warning: colors.yellow.darken3
      }
    },
    dark: false
  }
};

export default new Vuetify(opts);
