// Token key
const BGM_KEY = "bgm";

const saveSession = session => {
  if (session) {
    localStorage.setItem(BGM_KEY, JSON.stringify(session));
  } else {
    localStorage.removeItem(BGM_KEY);
  }
};
const retrieveSession = () => {
  return JSON.parse(localStorage.getItem(BGM_KEY));
};

const GET_SESSION = "GET_SESSION";
const SET_SESSION = "SET_SESSION";
const SET_SESSION_FROM_STORAGE = "SET_SESSION_FROM_STORAGE";
const CLEAR_SESSION = "CLEAR_SESSION";

const SET_USER = "SET_USER";
const SET_ROOM = "SET_ROOM";

export { GET_SESSION, SET_SESSION, retrieveSession, CLEAR_SESSION };

export default {
  state: {
    user_id: null,
    username: null,
    sid: null,
    room: null
  },
  mutations: {
    [SET_SESSION_FROM_STORAGE](state, session) {
      state.user_id = session.user_id;
      state.username = session.username;
    },
    [SET_USER](state, user) {
      state.user_id = user.user_id;
      state.username = user.username;
      state.sid = user.sid;
    },
    [SET_ROOM](state, room) {
      state.room = room.id;
    },
    [CLEAR_SESSION](state) {
      state.room = null;
      state.sid = null;
    }
  },
  actions: {
    [GET_SESSION]({ commit }) {
      const session = retrieveSession();
      if (session) commit(SET_SESSION_FROM_STORAGE, session);
    },
    [SET_SESSION]({ commit }, { user, room }) {
      saveSession({ ...user, room: room.id });
      commit(SET_USER, user);
      commit(SET_ROOM, room);
    }
  },
  getters: {
    user_id: state => {
      return state.user_id;
    }
  }
};
