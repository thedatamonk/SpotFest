import { createStore } from 'vuex';

// Create a new store instance
const store = createStore({
  state: {
    isLoggedIn: false,
  },
  mutations: {
    SET_LOGGED_IN(state, value) {
      state.isLoggedIn = value;
    }
  },
  actions: {
    logIn({commit}) {
      commit('SET_LOGGED_IN', true);
    }
  },
  getters: {}
});

export default store;
