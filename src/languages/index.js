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
// Regenwormen
import RWM_EN from "../games/regenwormen/languages/en.json";
import RWM_NL from "../games/regenwormen/languages/nl.json";
// Aet
import SET_EN from "../games/set_game/languages/en.json";
import SET_NL from "../games/set_game/languages/nl.json";

// Combine all translations
const en = { ...EN, ...GDT_EN, ...RWM_EN, ...SET_EN };
const nl = { ...NL, ...GDT_NL, ...RWM_NL, ...SET_NL };

const messages = {
  en,
  nl
};

const i18n = new VueI18n({
  locale: "en",
  messages
});

export default i18n;
