import Vue from "vue";
import VueI18n from "vue-i18n";

Vue.use(VueI18n);

// Import basic translations
import EN from "./en.json";
import NL from "./nl.json";

// Import translations from games
// GuessDiceThrow
import GDT_EN from "../games/guess_dice_throw/languages/en.json";
import GDT_NL from "../games/guess_dice_throw/languages/nl.json";

// Combine all translations
const en = { ...EN, ...GDT_EN };
const nl = { ...NL, ...GDT_NL };

const messages = {
  en,
  nl
};

const i18n = new VueI18n({
  locale: "en",
  messages
});

export default i18n;
