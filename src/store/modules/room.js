const INIT_ROOM = "INIT_ROOM";

const SET_ROOM_USERS = "SET_ROOM_USERS";
const SET_SETTINGS = "SET_SETTINGS";
const SET_CHAT = "SET_CHAT";
const SET_PASSWORD = "SET_PASSWORD";
const SET_GAME = "SET_GAME";

const UPDATE_CHAT = "UPDATE_CHAT";

export { INIT_ROOM, SET_CHAT, UPDATE_CHAT, SET_ROOM_USERS, SET_GAME };

export default {
  state: {
    id: null,
    users: [],
    messages: [],
    admin: null,
    password: null,
    settings: {
      max_size: 1
    },
    game: {}
  },
  mutations: {
    [SET_ROOM_USERS](state, room) {
      state.id = room.id;
      state.users = room.users;
      const admin = room.users.find(u => {
        return u.user_id === room.admin;
      });
      state.admin = admin ? admin.user_id : null;
    },
    [SET_CHAT](state, room) {
      state.messages = room.chat;
    },
    [SET_PASSWORD](state, room) {
      state.password = room.password;
    },
    [SET_SETTINGS](state, room) {
      state.settings = room.settings;
    },
    [UPDATE_CHAT](state, message) {
      state.messages = [...state.messages, message];
    },
    [SET_GAME](state, game) {
      state.game = game;
    }
  },
  actions: {
    [INIT_ROOM]({ commit }, room) {
      commit(SET_ROOM_USERS, room);
      commit(SET_CHAT, room);
      commit(SET_SETTINGS, room);
      commit(SET_PASSWORD, room);
      commit(SET_GAME, room.game);
    },
    [SET_ROOM_USERS]({ commit }, room) {
      commit(SET_ROOM_USERS, room);
    }
  },
  getters: {
    game: state => {
      return state.game.tag ? state.game : null;
    },
    admin: state => {
      return state.admin;
    }
  }
};
