const SET_GAMES_LIST = "SET_GAMES_LIST";

export { SET_GAMES_LIST };

export default {
  state: {
    available: []
  },
  mutations: {
    [SET_GAMES_LIST](state, games) {
      state.available = games;
    }
  },
  actions: {
    [SET_GAMES_LIST]({ commit }, games) {
      commit(SET_GAMES_LIST, games);
    }
  }
};
