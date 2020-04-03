import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import room from "./modules/room";
import games from "./modules/games";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user: user,
    room: room,
    games: games
  }
});
