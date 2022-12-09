import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'user_token': null,
  },
  getters: {
    getToken : state => {
      return state.user_token
    }
  },
  mutations: {
    setToken (state, token) {
      state.user_token = token
    },
    deleteToken (state) {
      state.user_token = null
    }
  },
  actions: {
  },
  modules: {
  }
})
